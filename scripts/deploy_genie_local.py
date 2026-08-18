#!/usr/bin/env python3
"""
Deploy Genie Space using Databricks SDK (works from workspace context)
Run this script from Databricks workspace, not from GitHub Actions
"""

import json
import sys
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dashboards import GenieSpace


def load_config(config_path: str):
    """Load Genie Space configuration"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_table_names(tables, catalog_name):
    """Update table names with target catalog"""
    return [
        table.replace('retail_ai3', catalog_name)
        for table in tables
    ]


def create_genie_space_sdk(catalog_name='retail_ai3_dev'):
    """Create Genie Space using Databricks SDK"""
    
    # Initialize Databricks client (uses workspace context)
    w = WorkspaceClient()
    
    # Load configuration
    config_path = '../genie/space_config.json'
    config = load_config(config_path)
    
    space_config = config['space']
    tables = update_table_names(config['tables'], catalog_name)
    
    print("=" * 70)
    print("🚀 Creating Genie Space using Databricks SDK")
    print("=" * 70)
    print(f"Display Name: {space_config['display_name']}")
    print(f"Catalog: {catalog_name}")
    print(f"Tables: {len(tables)}")
    print()
    
    try:
        # Create Genie Space
        # Note: SDK method may vary depending on version
        print("Creating space...")
        
        # Using Genie API endpoint
        space_data = {
            "display_name": space_config['display_name'],
            "description": space_config['description'],
            "table_identifiers": tables
        }
        
        # Call API through workspace client
        response = w.api_client.do(
            'POST',
            '/api/2.0/genie/spaces',
            body=space_data
        )
        
        space_id = response['space_id']
        print(f"✅ Space created: {space_id}")
        
        # Add starter questions
        print("\nAdding starter questions...")
        for q in config['starter_questions']:
            try:
                w.api_client.do(
                    'POST',
                    f'/api/2.0/genie/spaces/{space_id}/start-questions',
                    body={'content': q['question']}
                )
                print(f"  ✅ {q['question'][:60]}...")
            except Exception as e:
                print(f"  ⚠️  Skipped: {e}")
        
        print("\n" + "=" * 70)
        print(f"✅ Deployment completed!")
        print(f"Space ID: {space_id}")
        print(f"Access: https://dbc-9e376111-e24d.cloud.databricks.com/genie/rooms/{space_id}")
        print("=" * 70)
        
        return space_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    # Default to dev catalog
    catalog = sys.argv[1] if len(sys.argv) > 1 else 'retail_ai3_dev'
    create_genie_space_sdk(catalog)
