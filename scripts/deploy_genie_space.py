#!/usr/bin/env python3
"""
Deploy Genie Space to Databricks workspace
Reads configuration from genie/space_config.json
"""

import json
import os
import re
import sys
from urllib.parse import urlparse

import requests
from typing import Dict, List, Any


def normalize_workspace_url(workspace_url: str) -> str:
    """Normalize a Databricks workspace URL and reject API endpoints."""
    if not workspace_url:
        raise ValueError("DATABRICKS_HOST is empty")

    url = workspace_url.strip().rstrip('/')
    parsed = urlparse(url)

    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        raise ValueError(f"DATABRICKS_HOST must be a valid Databricks workspace URL: {workspace_url}")

    if parsed.path and parsed.path not in ('', '/'):
        raise ValueError(
            "DATABRICKS_HOST must be the workspace base URL, not an API URL. "
            f"Received: {workspace_url}"
        )

    if not re.search(r'\.cloud\.databricks\.com$|\.azuredatabricks\.net$', parsed.netloc):
        raise ValueError(f"DATABRICKS_HOST does not look like a Databricks workspace URL: {workspace_url}")

    return url


class GenieSpaceDeployer:
    def __init__(self, workspace_url: str, token: str, catalog_name: str, warehouse_id: str = None):
        self.workspace_url = normalize_workspace_url(workspace_url)
        self.token = token.strip()
        self.catalog_name = catalog_name
        self.warehouse_id = (warehouse_id or os.environ.get('WAREHOUSE_ID') or '').strip()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load Genie Space configuration from JSON file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_table_names(self, tables: List[str]) -> List[str]:
        """Update table names with target catalog"""
        return [
            table.replace('retail_ai3', self.catalog_name)
            for table in tables
        ]
    
    def update_sql_queries(self, benchmarks: List[Dict]) -> List[Dict]:
        """Update SQL queries with target catalog"""
        updated = []
        for benchmark in benchmarks:
            updated_benchmark = benchmark.copy()
            if 'expected_sql' in updated_benchmark:
                updated_benchmark['expected_sql'] = updated_benchmark['expected_sql'].replace(
                    'retail_ai3', self.catalog_name
                )
            updated.append(updated_benchmark)
        return updated
    
    def create_space(self, config: Dict[str, Any]) -> str:
        """Create Genie Space"""
        space_config = config['space']
        tables = self.update_table_names(config['tables'])
        
        if not self.warehouse_id:
            raise ValueError("WAREHOUSE_ID is required to create a Genie Space.")

        genie_space = {
            "display_name": space_config['display_name'],
            "description": space_config['description'],
            "table_identifiers": tables,
            "warehouse_id": self.warehouse_id
        }

        payload = {
            **genie_space,
            "serialized_space": json.dumps(genie_space)
        }
        
        print(f"Creating Genie Space: {space_config['display_name']}")
        print(f"Tables: {', '.join(tables)}")
        
        response = requests.post(
            f"{self.workspace_url}/api/2.0/genie/spaces",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            print(f"Error creating space: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        space_id = response.json()['space_id']
        print(f"✅ Space created with ID: {space_id}")
        return space_id
    
    def add_starter_questions(self, space_id: str, questions: List[Dict]):
        """Add starter questions to Genie Space"""
        print("\nAdding starter questions...")
        for q in questions:
            payload = {
                "content": q['question']
            }
            
            response = requests.post(
                f"{self.workspace_url}/api/2.0/genie/spaces/{space_id}/start-questions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"  ✅ Added: {q['question'][:60]}...")
            else:
                print(f"  ❌ Failed: {q['question'][:60]}...")
                print(f"     Error: {response.text}")
    
    def add_benchmarks(self, space_id: str, benchmarks: List[Dict]):
        """Add benchmark questions to Genie Space"""
        print("\nAdding benchmark questions...")
        updated_benchmarks = self.update_sql_queries(benchmarks)
        
        for b in updated_benchmarks:
            payload = {
                "question": b['question'],
                "expected_sql": b['expected_sql']
            }
            
            response = requests.post(
                f"{self.workspace_url}/api/2.0/genie/spaces/{space_id}/benchmarks",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"  ✅ Added: {b['question'][:60]}...")
            else:
                print(f"  ⚠️  Skipped: {b['question'][:60]}...")
                # Benchmark API might not be available in all workspaces
    
    def deploy(self, config_path: str):
        """Deploy complete Genie Space"""
        print("=" * 70)
        print("Genie Space Deployment")
        print("=" * 70)
        print(f"Workspace: {self.workspace_url}")
        print(f"Catalog: {self.catalog_name}")
        print()
        
        config = self.load_config(config_path)
        
        # Create space
        space_id = self.create_space(config)
        
        # Add starter questions
        if 'starter_questions' in config:
            self.add_starter_questions(space_id, config['starter_questions'])
        
        # Add benchmarks
        if 'benchmark_questions' in config:
            self.add_benchmarks(space_id, config['benchmark_questions'])
        
        print("\n" + "=" * 70)
        print(f"✅ Deployment completed!")
        print(f"Space ID: {space_id}")
        print(f"Space URL: {self.workspace_url}/genie/rooms/{space_id}")
        print("=" * 70)


def main():
    # Get configuration from environment
    workspace_url = os.environ.get('DATABRICKS_HOST')
    token = os.environ.get('DATABRICKS_TOKEN')
    warehouse_id = os.environ.get('WAREHOUSE_ID') or '5b8e2cea7c9d6bbf'
    catalog_name = os.environ.get('CATALOG_NAME', 'retail_ai3')

    if not workspace_url or not token:
        print("Error: DATABRICKS_HOST and DATABRICKS_TOKEN must be set")
        sys.exit(1)

    try:
        workspace_url = normalize_workspace_url(workspace_url)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    if not token.startswith(('dapi', 'dap')):
        print("Error: DATABRICKS_TOKEN appears invalid. Databricks personal access tokens usually start with 'dapi'.")
        sys.exit(1)

    # Path to config file
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'genie',
        'space_config.json'
    )

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    # Deploy
    deployer = GenieSpaceDeployer(workspace_url, token, catalog_name, warehouse_id)
    deployer.deploy(config_path)


if __name__ == '__main__':
    main()
