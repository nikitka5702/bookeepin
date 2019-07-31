import React, { Component, Fragment } from 'react'
import Moment from 'react-moment'
import { Row, Alert, Tag, Button } from 'antd'
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

  setAccountId = accountId => this.setState({accountId})

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
            width: Math.floor(document.documentElement.clientWidth *.15),
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

export default Incomes
