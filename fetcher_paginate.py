# Python 3.6+
# pip(3) install requests
import requests
import json

# Standard headers
HEADERS_AUTH = {"Content-Type": "application/x-www-form-urlencoded"}
HEADERS = {"Content-Type": "application/json"}

client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"

# Uncomment the following section to define the proxies in your environment,
#   if necessary:
# http_proxy  = "http://"+user+":"+passw+"@x.x.x.x:abcd"
# https_proxy = "https://"+user+":"+passw+"@y.y.y.y:abcd"
# proxyDict = {
#     "http"  : http_proxy,
#     "https" : https_proxy
# }

# The GraphQL query that defines which data you wish to fetch.

sub_id = ""
new_subs = []

subs_variables = {
  "quick": False,
  "fetchPublicExposurePaths": False,
  "fetchInternalExposurePaths": False,
  "fetchIssueAnalytics": False,
  "fetchLateralMovement": False,
  "fetchKubernetes": False,
  "first": 1000,
  "query": {
    "type": [
      "SUBSCRIPTION"
    ],
    "select": True
  },
  "projectId": "*",
  "fetchTotalCount": False
}

subs_query = ("""
    query GraphSearch(
        $query: GraphEntityQueryInput
        $controlId: ID
        $projectId: String!
        $first: Int
        $after: String
        $fetchTotalCount: Boolean!
        $quick: Boolean = true
        $fetchPublicExposurePaths: Boolean = false
        $fetchInternalExposurePaths: Boolean = false
        $fetchIssueAnalytics: Boolean = false
        $fetchLateralMovement: Boolean = false
        $fetchKubernetes: Boolean = false
      ) {
        graphSearch(
          query: $query
          controlId: $controlId
          projectId: $projectId
          first: $first
          after: $after
          quick: $quick
        ) {
          totalCount @include(if: $fetchTotalCount)
          maxCountReached @include(if: $fetchTotalCount)
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            entities {
              ...PathGraphEntityFragment
              userMetadata {
                isInWatchlist
                isIgnored
                note
              }
              technologies {
                id
                icon
              }
              publicExposures(first: 10) @include(if: $fetchPublicExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              otherSubscriptionExposures(first: 10)
                @include(if: $fetchInternalExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              otherVnetExposures(first: 10)
                @include(if: $fetchInternalExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              lateralMovementPaths(first: 10) @include(if: $fetchLateralMovement) {
                nodes {
                  id
                  pathEntities {
                    entity {
                      ...PathGraphEntityFragment
                    }
                  }
                }
              }
              kubernetesPaths(first: 10) @include(if: $fetchKubernetes) {
                nodes {
                  id
                  path {
                    ...PathGraphEntityFragment
                  }
                }
              }
            }
            aggregateCount
          }
        }
      }
  
      fragment PathGraphEntityFragment on GraphEntity {
        id
        name
        type
        properties
        issueAnalytics: issues(filterBy: { status: [IN_PROGRESS, OPEN] })
          @include(if: $fetchIssueAnalytics) {
          highSeverityCount
          criticalSeverityCount
        }
      }

  
      fragment NetworkExposureFragment on NetworkExposure {
        id
        portRange
        sourceIpRange
        destinationIpRange
        path {
          ...PathGraphEntityFragment
        }
        applicationEndpoints {
          ...PathGraphEntityFragment
        }
      }
""")

main_query = ("""
    query GraphSearch(
        $query: GraphEntityQueryInput
        $controlId: ID
        $projectId: String!
        $first: Int
        $after: String
        $fetchTotalCount: Boolean!
        $quick: Boolean = true
        $fetchPublicExposurePaths: Boolean = false
        $fetchInternalExposurePaths: Boolean = false
        $fetchIssueAnalytics: Boolean = false
        $fetchLateralMovement: Boolean = false
        $fetchKubernetes: Boolean = false
      ) {
        graphSearch(
          query: $query
          controlId: $controlId
          projectId: $projectId
          first: $first
          after: $after
          quick: $quick
        ) {
          totalCount @include(if: $fetchTotalCount)
          maxCountReached @include(if: $fetchTotalCount)
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            entities {
              ...PathGraphEntityFragment
              userMetadata {
                isInWatchlist
                isIgnored
                note
              }
              technologies {
                id
                icon
              }
              publicExposures(first: 10) @include(if: $fetchPublicExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              otherSubscriptionExposures(first: 10)
                @include(if: $fetchInternalExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              otherVnetExposures(first: 10)
                @include(if: $fetchInternalExposurePaths) {
                nodes {
                  ...NetworkExposureFragment
                }
              }
              lateralMovementPaths(first: 10) @include(if: $fetchLateralMovement) {
                nodes {
                  id
                  pathEntities {
                    entity {
                      ...PathGraphEntityFragment
                    }
                  }
                }
              }
              kubernetesPaths(first: 10) @include(if: $fetchKubernetes) {
                nodes {
                  id
                  path {
                    ...PathGraphEntityFragment
                  }
                }
              }
            }
            aggregateCount
          }
        }
      }
  
      fragment PathGraphEntityFragment on GraphEntity {
        id
        name
        type
        properties
        issueAnalytics: issues(filterBy: { status: [IN_PROGRESS, OPEN] })
          @include(if: $fetchIssueAnalytics) {
          highSeverityCount
          criticalSeverityCount
        }
      }

  
      fragment NetworkExposureFragment on NetworkExposure {
        id
        portRange
        sourceIpRange
        destinationIpRange
        path {
          ...PathGraphEntityFragment
        }
        applicationEndpoints {
          ...PathGraphEntityFragment
        }
      }
""")

def run_subs_query(subs_query, subs_variables, new_subs):
    """Query WIZ API for the given query data schema"""
    data = {"variables": subs_variables, "query": subs_query}

    try:
        # Uncomment the next first line and comment the line after that
        # to run behind proxies
        # result = requests.post(url="https://api.us20.app.wiz.io/graphql",
        #                        json=data, headers=HEADERS, proxies=proxyDict)

        result = requests.post(url="https://api.us20.app.wiz.io/graphql",
                               json=data, headers=HEADERS)
        for sub in result.json()["data"]["graphSearch"]["nodes"]:
            new_subs.append(sub["entities"][0]["properties"]["externalId"])
        
        pageInfo = result.json()['data']['graphSearch']['pageInfo']
        
        while (pageInfo['hasNextPage']):
            # fetch next page
            subs_variables['after'] = pageInfo['endCursor']
            result = run_subs_query(subs_query, subs_variables)
            for sub in result.json()["data"]["graphSearch"]["nodes"]:
              new_subs.append(sub["entities"][0]["properties"]["externalId"])
            
            pageInfo = result.json()['data']['graphSearch']['pageInfo']

    except Exception as e:
        if ('502: Bad Gateway' not in str(e) and
                '503: Service Unavailable' not in str(e) and
                '504: Gateway Timeout' not in str(e)):
            print("<p>Wiz-API-Error: %s</p>" % str(e))
            return(e)
        else:
            print("Retry")

def run_main_query(subscription_id):
    sub_id = subscription_id

    main_variables = {
      "quick": False,
      "fetchPublicExposurePaths": True,
      "fetchInternalExposurePaths": False,
      "fetchIssueAnalytics": False,
      "fetchLateralMovement": True,
      "fetchKubernetes": False,
      "first": 1000,
      "query": {
        "type": [
          "CONTAINER"
        ],
        "select": True,
        "relationships": [
          {
            "type": [
              {
                "type": "INSTANCE_OF"
              }
            ],
            "with": {
              "type": [
                "CONTAINER_IMAGE"
              ],
              "select": True,
              "relationships": [
                {
                  "type": [
                    {
                      "type": "RUNS"
                    }
                  ],
                  "with": {
                    "type": [
                      "HOSTED_TECHNOLOGY"
                    ],
                    "select": True,
                    "relationships": [
                      {
                        "type": [
                          {
                            "type": "HAS_TECH"
                          }
                        ],
                        "with": {
                          "type": [
                            "TECHNOLOGY"
                          ],
                          "select": True,
                          "where": {
                            "categories": {
                              "EQUALS": [
                                "Operating System"
                              ]
                            }
                          }
                        }
                      }
                    ],
                    "where": {
                      "isVersionEndOfLife": {
                        "EQUALS": True
                      }
                    }
                  }
                }
              ]
            }
          },
          {
            "type": [
              {
                "type": "CONTAINS",
                "reverse": True
              }
            ],
            "with": {
              "type": [
                "SUBSCRIPTION"
              ],
              "select": True,
              "where": {
                "externalId": {
                  "EQUALS": [
                    sub_id
                  ]
                }
              }
            }
          }
        ]
      },
      "projectId": "*",
      "fetchTotalCount": False
  }
    data = {"variables": main_variables, "query" : main_query}

    try:
      #     # Uncomment the next first line and comment the line after that
      #     # to run behind proxies
      #     # result = requests.post(url="https://api.us20.app.wiz.io/graphql",
      #     #                        json=data, headers=HEADERS, proxies=proxyDict)

      result = requests.post(url="https://api.us20.app.wiz.io/graphql",
                              json=data, headers=HEADERS)

      write_csv(result.json()["data"]["graphSearch"]["nodes"])

      pageInfo = result.json()['data']['graphSearch']['pageInfo']
      while (pageInfo['hasNextPage']):
          # fetch next page
          subs_variables['after'] = pageInfo['endCursor']
          result = run_main_query(subscription_id)
          write_csv(result.json()["data"]["graphSearch"]["nodes"])
          pageInfo = result.json()['data']['graphSearch']['pageInfo']

    except IndexError:
        print("No results found for subscription_id: " + subscription_id)
    except Exception as e:
      if ('502: Bad Gateway' not in str(e) and
              '503: Service Unavailable' not in str(e) and
              '504: Gateway Timeout' not in str(e)):
          print("<p>Wiz-API-Error: %s</p>" % str(e))
          return(e)
      else:
          print("Retry")


def request_wiz_api_token(client_id, client_secret):
    """Retrieve an OAuth access token to be used against Wiz API"""
    auth_payload = {
      'grant_type': 'client_credentials',
      'audience': 'wiz-api',
      'client_id': client_id,
      'client_secret': client_secret
    }
    # Uncomment the next first line and comment the line after that
    # to run behind proxies
    # response = requests.post(url="https://auth.app.wiz.io/oauth/token",
    #                         headers=HEADERS_AUTH, data=auth_payload,
    #                         proxies=proxyDict)
    response = requests.post(url="https://auth.app.wiz.io/oauth/token",
                             headers=HEADERS_AUTH, data=auth_payload)

    if response.status_code != requests.codes.ok:
        raise Exception('Error authenticating to Wiz [%d] - %s' %
                        (response.status_code, response.text))

    try:
        response_json = response.json()
        TOKEN = response_json.get('access_token')
        if not TOKEN:
            message = 'Could not retrieve token from Wiz: {}'.format(
                    response_json.get("message"))
            raise Exception(message)
    except ValueError as exception:
        print(exception)
        raise Exception('Could not parse API response')
    HEADERS["Authorization"] = "Bearer " + TOKEN

    return TOKEN

def write_csv(results):
    
    print("FOUND RESULTS: " + str(len(results)))
    csv_file = open("results.csv", "a")
    
    for result in results:
      # if  result["entities"][0]["type"] != "CONTAINER":
      #     print("Found 0 != CONTAINER")

      # if  result["entities"][1]["type"] != "CONTAINER_IMAGE":
      #     print("Found 1 != CONTAINER_IMAGE")     
      
      # if  result["entities"][2]["type"] != "HOSTED_TECHNOLOGY":
      #     print("Found 2 != HOSTED_TECHNOLOGY")

      # if  result["entities"][3]["type"] != "TECHNOLOGY":
      #     print("Found 3 != TECHNOLOGY")

      # if  result["entities"][4]["type"] != "SUBSCRIPTION":
      #     print("Found 4 != SUBSCRIPTION")

      csv_file.write(result["entities"][4]["properties"]["cloudPlatform"] + "," + result["entities"][4]["properties"]["externalId"] + "," + result["entities"][0]["name"] + "," + result["entities"][0]["properties"]["externalId"] + "," + result["entities"][1]["properties"]["externalId"] + "," + result["entities"][3]["name"] + "," + result["entities"][2]["properties"]["version"] + "," + str(result["entities"][2]["properties"]["isVersionEndOfLife"]) + "\n")
    
    csv_file.close()


def process_subscription(subscription_id):

    result = run_main_query(subscription_id)


def main():

    print("Getting token.")
    request_wiz_api_token(client_id, client_secret)


    print("Writing headings to file...")
    csv_file = open("results.csv", "w")
    csv_file.write("Cloud Platform, Subscription External ID,Container Name, Container External ID, Container Image externalID, Container OS, Container OS Version, isOSEOL\n")
    csv_file.close()

    print("Fetching subscriptions...")

    run_subs_query(subs_query, subs_variables, new_subs)

    print("Fetched subscriptions.")

    for subscription_id in new_subs:
        print("Processing subscription " + subscription_id )
        process_subscription(subscription_id)
    
if __name__ == '__main__':
    main()