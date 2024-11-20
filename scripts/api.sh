#!/bin/bash

BUNDLE_ALIAS=
API_KEY=
ALL_CONTACTS_VIEW_ID=
ALL_ACCOUNTS_VIEW_ID=
ALL_DEALS_VIEW_ID=

# Query All Views
# curl -H "Authorization: Token token=$API_KEY" -H "Content-Type: application/json" -X GET "https://$BUNDLE_ALIAS/api/contacts/view/$ALL_CONTACTS_VIEW_ID" | jq . > temp/contacts.json
# curl -H "Authorization: Token token=$API_KEY" -H "Content-Type: application/json" -X GET "https://$BUNDLE_ALIAS/api/sales_accounts/view/$ALL_ACCOUNTS_VIEW_ID?include=contacts" | jq . > temp/accounts.json
# curl -H "Authorization: Token token=$API_KEY" -H "Content-Type: application/json" -X GET "https://$BUNDLE_ALIAS/api/deals/view/$ALL_DEALS_VIEW_ID?include=sales_account" | jq . > temp/deals.json

# curl -H "Authorization: Token token=$API_KEY" -H "Content-Type: application/json" -X GET "https://$BUNDLE_ALIAS/api/sales_accounts/view/$ALL_ACCOUNTS_VIEW_ID?page=1&include=contacts" | jq . > temp/accounts.json

DEAL_ID="202000322319"
NEW_DEAL_SIZE="24456"


# Upsert a deal
curl -H "Authorization: Token token=$API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "unique_identifier": {
               "id": "'$DEAL_ID'"
           },
           "deal": {
               "custom_field": {
                   "cf_deal_size": "'$NEW_DEAL_SIZE'"
               }
           }
         }' \
     -X POST "https://$BUNDLE_ALIAS/api/deals/upsert"
