from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from config import config

END_POINT_URL = f'http://{config.HOST}:8000/graphql/'
METHOD = 'POST'


def get_client(token=None):
    if not token:
        _transport = RequestsHTTPTransport(
            url=END_POINT_URL,
        )
    else:
        _transport = RequestsHTTPTransport(
            url=END_POINT_URL,
            headers={'Authorization': f'JWT {token}'}
        )
    client = Client(
        transport=_transport,
    )
    return client


def sign_in(username, password):
    query = gql(r"""
    mutation {
        tokenAuth(username: "%s", password: "%s") {
            token
        }
    }
    """ % (username, password))

    try:
        response = get_client().execute(query)
        response = response.get('tokenAuth')
        return response['token']
    except Exception as e:
        return None


def create_category(category_type, category_description, token):
    query = gql(r"""
        mutation {
          createCategory(categoryType: "%s", description: "%s"){
            category{
              id
              description
            }
          }
        }
    """ % (category_type, category_description))
    try:
        response = get_client(token).execute(query)
        response = response.get('createCategory').get('category')
        return int(response['id'])
    except Exception as e:
        return None


def get_accounts_dict(token):
    query = gql(r"""
            query {
              accounts{
                id
                description
              }
            }
        """)
    try:
        response = get_client(token).execute(query)
        response = response.get('accounts')
        accounts = {}

        for category in response:
            accounts[int(category.get('id'))] = category.get('description')

        return accounts
    except Exception as e:
        return {}


def get_categories_dict(categories_type, token):
    query = gql(r"""
            query {
              categories(categoryType: "%s"){
                id
                description
              }
            }
        """ % (categories_type))
    try:
        response = get_client(token).execute(query)
        response = response.get('categories')
        categories = {}

        for category in response:
            categories[int(category.get('id'))] = category.get('description')

        return categories
    except Exception as e:
        return {}


def create_income(token, data: dict):
    args = ''
    for key, value in data.items():
        if isinstance(value, str):
            args += f'{key}: "{value}", '
        else:
            args += f'{key}: {value}, '

    query = gql(r"""
                mutation {
                  createIncome(%s){
                    income{
                      id
                    }
                  }
                }
            """ % (args[:-2]))
    try:
        get_client(token).execute(query)
        return True
    except Exception as e:
        return False


def create_expense(token, data):
    args = ''
    for key, value in data.items():
        if isinstance(value, str):
            args += f'{key}: "{value}", '
        else:
            args += f'{key}: {value}, '

    query = gql(r"""
                    mutation {
                      createExpense(%s){
                        expense{
                          id
                        }
                      }
                    }
                """ % (args[:-2]))
    try:
        get_client(token).execute(query)
        return True
    except Exception as e:
        return False