import React, { Component, Fragment } from 'react'
import Moment from 'react-moment'
import { Row, Alert, Tag } from 'antd'
import gql from 'graphql-tag'

import Records from '../layout/Records'
import AccountMenu from '../layout/AccountMenu'


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

const TOTAL_EXPENSES = gql`
query TotalExpenses($accountId: Int!, $search: String, $first: Int!, $skip: Int!) {
  totalExpenses(accountId: $accountId, search: $search, first: $first, skip: $skip) {
    expenses {
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

const CREATE_EXPENSE = gql`
mutation CreateExpense($accountId: Int!, $description: String!, $amount: Float!, $date: Date!, $groupId: Int!, $cashBack: Float!) {
  createExpense(account: $accountId, description: $description, amount: $amount, date: $date, group: $groupId, cashBack: $cashBack) {
    expense {
      id
    }
  }
}
`

const UPDATE_EXPENSE = gql`
mutation UpdateExpense($id: Int!, $expenseData: ExpenseInput) {
  updateExpense(id: $id, expenseData: $expenseData) {
    expense {
      id
    }
  }
}
`

const DELETE_EXPENSE = gql`
mutation DeleteExpense($id: Int!) {
  deleteExpense(id: $id) {
    result
  }
}
`

class Expenses extends Component {
  state = {
    accountId: 0
  }

  setAccountId = accountId => this.setState({accountId})

  render() {
    const accountBody = this.state.accountId === 0 ? (
      <Row type="flex" justify="center" align="middle" style={{height: '100%'}}>
        <Alert message="Select account" type="info" showIcon/>
      </Row>
    ) : (
      <Records
        accountId={this.state.accountId}
        name="Expenses"
        qName="totalExpenses"
        qObjects="expenses"
        query={TOTAL_EXPENSES}
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
            width: Math.floor(document.documentElement.clientWidth * .20),
            key: 'groupName',
            render: text => <Tag color="purple">{text}</Tag>
          },
          {
            title: 'Edit',
            dataIndex: 'edit',
            key: 'edit',
          }
        ]}
        modals={{
          add: <Fragment />,
          edit: <Fragment />,
          delete: <Fragment />
        }}
      />
    )

    return (
      <AccountMenu
        query={TOTAL_ACCOUNTS}
        menuSelect={this.setAccountId}
      >
        {accountBody}
      </AccountMenu>
    )
  }
}

export default Expenses
