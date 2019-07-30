import React, { Component, Fragment } from 'react'
import Moment from 'react-moment'
import { Formik, ErrroMessage } from 'formik'
import { Layout, Pagination, Spin, Row, Col, Alert, Menu, Tag, Icon } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

import Records from '../layout/Records'

const { Content, Header } = Layout

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
query TotalIncomes($accountId: Int!, $search: String, $first: Int!, $skip: Int!) {
  totalIncomes(accountId: $accountId, search: $search, first: $first, skip: $skip) {
    incomes {
      id
      description
      amount
      date
      group {
        name
      }
    }
    total
  }
}
`

const CREATE_INCOME = gql`
mutation CreateIncome($accountId: Int!, $description: String!, $amount: Float!, $date: Date!, $groupId: Int!) {
  createIncome(account: $accountId, description: $description, amount: $amount, date: $date, group: $groupId) {
    income {
      id
    }
  }
}
`

const UPDATE_INCOME = gql`
mutation UpdateIncome($id: Int!, $incomeData: IncomeInput) {
  updateIncome(id: $id, incomeData: $incomeData) {
    income {
      id
    }
  }
}
`

const DELETE_INCOME = gql`
mutation DeleteIncome($id: Int!) {
  deleteIncome(id: $id) {
    result
  }
}
`

class Incomes extends Component {
  state = {
    accountId: 0
  }

  render() {
    const accountBody = this.state.accountId === 0 ? (
      <Row type="flex" justify="center" align="middle" style={{height: '100%'}}>
        <Alert message="Select account" type="info" showIcon/>
      </Row>
    ) : (
      <Records
        accountId={this.state.accountId}
        name="Incomes"
        qName="totalIncomes"
        qObjects="incomes"
        query={TOTAL_INCOMES}
        fields={{
          key: ['id'],
          description: ['description'],
          amount: ['amount'],
          date: ['date'],
          groupName: ['name', 'group']
        }}
        columns={[
          {
            title: 'Description',
            dataIndex: 'description',
            width: Math.floor(document.documentElement.clientWidth * .15),
            key: 'description'
          },
          {
            title: 'Amount',
            dataIndex: 'amount',
            width: Math.floor(document.documentElement.clientWidth * .10),
            key: 'amount'
          },
          {
            title: 'Date',
            dataIndex: 'date',
            width: Math.floor(document.documentElement.clientWidth * .15),
            key: 'date',
            render: date => <Moment format="Do MMMM YYYY">{date}</Moment>
          },
          {
            title: 'Group Name',
            dataIndex:'groupName',
            key: 'groupName',
            render: text => <Tag color="purple">{text}</Tag>
          }
        ]}
        mutations={{
          add: CREATE_INCOME,
          edit: UPDATE_INCOME,
          delete: DELETE_INCOME
        }}
        validators={{
          add: Yup.object().shape({}),
          edit: Yup.object().shape({}),
          delete: Yup.object().shape({})
        }}
      />
    )

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
              fetchPolicy='network-only'
            >
              {({ loading, error, data }) => {
                if (loading) return (
                  <Row type="flex" justify="center" align="middle" style={{height: '100%'}}>
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
                    onClick={({ key }) => this.setState({accountId: Number.parseInt(key)})}
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
              padding: 24
            }}
          >
            {accountBody}
          </Content>
        </Layout>
      </Content>
    )
  }
}

export default Incomes
