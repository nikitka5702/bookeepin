import React, { Component, Fragment } from 'react'
import { Formik, ErrroMessage } from 'formik'
import { Layout, Pagination, Spin, Row, Col, Alert } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

const { Content } = Layout

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
        <Query 
          query={TOTAL_INCOMES}
          variables={{first: this.state.pageSize, skip: (this.state.page - 1) * this.state.pageSize}}
          pollInterval={500}
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
              <Fragment>
                <Row>
                </Row>
                <Row type="flex" justify="center">
                  <Pagination
                    showSizeChanger
                    current={this.state.page}
                    defaultPageSize={this.state.pageSize}
                    onShowSizeChange={this.setPageSize}
                    onChange={page => this.setState({page})}
                    defaultCurrent={this.state.page}
                    total={data.totalIncomes.total}
                  />
                </Row>
              </Fragment>
            )
          }}
        </Query>
      </Content>
    )
  }
}

export default Incomes
