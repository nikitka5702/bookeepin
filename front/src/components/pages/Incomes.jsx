import React, { Component, Fragment } from 'react'
import { Formik, ErrroMessage } from 'formik'
import { Layout, Pagination, Spin, Row, Col, Alert, Menu } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

import Income from '../layout/Income'

const { Content } = Layout

const TOTAL_ACCOUNTS = gql`
query {
  totalAccounts {
    accounts {
      id
      description
    }
  }
}
`

const TOTAL_INCOMES = gql`
query TotalIncomes($search: String, $first: Int!, $skip: Int!) {
  totalIncomes(search: $search, first: $first, skip: $skip) {
    incomes {
      id
      account {
        id
        amount
        description
      }
      description
      amount
      date
      group {
        id
        categoryType
        name
      }
    }
    total
  }
}
`

class Incomes extends Component {
  state = {
    accountId: 0,
    page: 1,
    pageSize: 10
  }

  setPageSize = (_, size) => this.setState({pageSize: size})

  setCurrentPage = page => this.setState({page})

  render() {
    return (
      <Content
        style={{
          margin: '24px 16px',
          padding: 24,
          background: '#fff'
        }}
      >
        <Layout style={{ height: '100%' }}>
          <Layout.Sider>
            <Query
              query={TOTAL_ACCOUNTS}
              pollInterval={5000}
            >
              {({ loading, error, data }) => {
                if (loading) return (
                  <Row type="flex" justify="center">
                    <Spin size="large" />
                  </Row>
                )
                if (error) return (
                  <Row type="flex" justify="center">
                    <Alert message={`Error! ${error.message}`} type="error" />
                  </Row>
                )

                return (
                  <Menu
                    mode="inline"
                    style={{ height: '100%' }}
                    onClick={({ key }) => console.log(key)}
                  >
                    {data.totalAccounts.accounts.map(account => (
                      <Menu.Item key={account.id}>{account.description}</Menu.Item>
                    ))}
                  </Menu>
                )
              }}
            </Query>
          </Layout.Sider>
          <Content
            style={{
              padding: 24,
              background: '#ccc'
            }}
          >
            <Income account_id={this.state.accountId} />
          </Content>
        </Layout>
      </Content>
    )
  }
}

export default Incomes
