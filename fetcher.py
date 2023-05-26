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

def run_subs_query():
    """Query WIZ API for the given query data schema"""
    data = {"variables": {
  "quick": False,
  "fetchPublicExposurePaths": False,
  "fetchInternalExposurePaths": False,
  "fetchIssueAnalytics": False,
  "fetchLateralMovement": False,
  "fetchKubernetes": False,
  "first": 500,
  "query": {
    "type": [
      "SUBSCRIPTION"
    ],
    "select": True
  },
  "projectId": "*",
  "fetchTotalCount": False
}, "query": ("""
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
""")}

    try:
        # Uncomment the next first line and comment the line after that
        # to run behind proxies
        # result = requests.post(url="https://api.us20.app.wiz.io/graphql",
        #                        json=data, headers=HEADERS, proxies=proxyDict)
        result = requests.post(url="https://api.us20.app.wiz.io/graphql",
                               json=data, headers=HEADERS)

    except Exception as e:
        if ('502: Bad Gateway' not in str(e) and
                '503: Service Unavailable' not in str(e) and
                '504: Gateway Timeout' not in str(e)):
            print("<p>Wiz-API-Error: %s</p>" % str(e))
            return(e)
        else:
            print("Retry")

    return json.dumps(result.json())

def run_main_query(subscription_id):
    data = {"variables": {
  "quick": True,
  "fetchPublicExposurePaths": True,
  "fetchInternalExposurePaths": False,
  "fetchIssueAnalytics": False,
  "fetchLateralMovement": True,
  "fetchKubernetes": False,
  "first": 500,
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
                subscription_id
              ]
            }
          }
        }
      }
    ]
  },
  "projectId": "*",
  "fetchTotalCount": False
}, "query" : ("""
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
""")}

    try:
        # Uncomment the next first line and comment the line after that
        # to run behind proxies
        # result = requests.post(url="https://api.us20.app.wiz.io/graphql",
        #                        json=data, headers=HEADERS, proxies=proxyDict)

        result = requests.post(url="https://api.us20.app.wiz.io/graphql",
                               json=data, headers=HEADERS)    

        return result.json()    

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

def fetch_subscriptions():

    new_subs = []

    subs = json.loads(run_subs_query())

    for sub in subs["data"]["graphSearch"]["nodes"]:
        new_subs.append(sub["entities"][0]["properties"]["externalId"])

    return new_subs

def generate_csv(results):

    csv_file = open("results.csv", "a")
    for result in results["data"]["graphSearch"]["nodes"]:

        # if result["entities"][0]["type"] != "CONTAINER":
        #     print("Found 0 != CONTAINER")

        # if result["entities"][1]["type"] != "CONTAINER_IMAGE":
        #     print("Found 1 != CONTAINER_IMAGE")     
        
        # if result["entities"][2]["type"] != "HOSTED_TECHNOLOGY":
        #     print("Found 2 != HOSTED_TECHNOLOGY")

        # if result["entities"][3]["type"] != "TECHNOLOGY":
        #     print("Found 3 != TECHNOLOGY")

        # if result["entities"][4]["type"] != "SUBSCRIPTION":
        #     print("Found 4 != SUBSCRIPTION")

        print("Cloud Platform: " + result["entities"][4]["properties"]["cloudPlatform"])

        csv_file.write(result["entities"][4]["properties"]["cloudPlatform"] + "," + result["entities"][4]["properties"]["externalId"] + "," + result["entities"][0]["name"] + "," + result["entities"][0]["properties"]["externalId"] + "," + result["entities"][1]["properties"]["externalId"] + "," + result["entities"][3]["name"] + "," + result["entities"][2]["properties"]["version"]+"\n")


def process_subscription(subscription_id):

    result = run_main_query(subscription_id)

    print(result)

    generate_csv(result)

def main():

    print("Getting token.")
    request_wiz_api_token(client_id, client_secret)

    print("Fetching subscriptions...")

    subs = fetch_subscriptions()

    print("Fetched subscriptions.")

    csv_file = open("results.csv", "w")
    csv_file.write("Subscription External ID,Container Name, Container External ID, Container Image externalID, Container OS, Container OS Version, isOSEOL\n")


    for subscription_id in subs:
        print("Processing subscription " + subscription_id )
        process_subscription(subscription_id)
    
    
    # your data is here!

    # The above code lists the first <x> items.
    # If paginating on a Graph Query,
    #   then use <'quick': False> in the query variables.
    # Uncomment the following section to paginate over all the results:
    # pageInfo = result['data']['graphSearch']['pageInfo']
    # while (pageInfo['hasNextPage']):
    #     # fetch next page
    #     variables['after'] = pageInfo['endCursor']
    #     result = query_wiz_api(query, variables)
    #     print(result)
    #     pageInfo = result['data']['graphSearch']['pageInfo']


if __name__ == '__main__':
    main()