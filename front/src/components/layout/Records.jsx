import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { Formik, ErrroMessage } from 'formik'
import { Pagination, Spin, Row, Col, Alert, Table } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

import lookup from '../../helper'

class Records extends Component {
  static propTypes = {
    accountId: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    qName: PropTypes.string.isRequired,
    qObjects: PropTypes.string.isRequired,
    query: PropTypes.object.isRequired,
    fields: PropTypes.objectOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
    columns: PropTypes.arrayOf(PropTypes.objectOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.func]))).isRequired,
    mutations: PropTypes.exact({
      add: PropTypes.object.isRequired,
      edit: PropTypes.object.isRequired,
      delete: PropTypes.object.isRequired
    }).isRequired,
    validators: PropTypes.exact({
      add: PropTypes.instanceOf(Yup.object).isRequired,
      edit: PropTypes.instanceOf(Yup.object).isRequired,
      delete: PropTypes.instanceOf(Yup.object).isRequired
    }).isRequired
  }

  state = {
    page: 1,
    pageSize: 10
  }

  render() {
    const { accountId, name, qName, qObjects, query, fields, columns, mutations, validators } = this.props
    const { page, pageSize } = this.state

    return (
      <Query
        query={query}
        variables={{accountId: accountId, first: pageSize, skip: (page - 1) * pageSize}}
        pollInterval={5000}
      >
        {({ loading, error, data }) => {
          if (loading) return (
            <Row type="flex" justify="center" align="middle" style={{height: '100%'}}>
              <Spin size="large" />
            </Row>
          )
          if (error) return (
            <Row type="flex" justify="center" align="middle" style={{height: '100%'}}>
              <Alert message={`Error! ${error.message}`} type="error" />
            </Row>
          )

          return (
            <Fragment>
              <Row type="flex" justify="center" align="middle" style={{height: '5%'}}>
                {name}
              </Row>
              <Row type="flex" justify="center" align="top" style={{height: '85%', width: '100%'}}>
                <Table
                  style={{width: '100%'}}
                  columns={columns}
                  pagination={false}
                  scroll={{
                    y: Math.floor(document.documentElement.clientHeight * .61)
                  }}
                  dataSource={data[qName][qObjects].map((value, i) => {
                    let o = {}
                    for (let key in fields) {
                      o[key] = lookup(fields[key], value)
                    }

                    return o
                  })}
                />
              </Row>
              <Row type="flex" justify="center" align="middle" style={{height: '10%'}}>
                <Pagination
                  showSizeChanger
                  current={page}
                  defaultPageSize={pageSize}
                  onShowSizeChange={(_, pageSize) => this.setState({pageSize})}
                  onChange={page => this.setState({page})}
                  total={data[qName].total}
                />
              </Row>
            </Fragment>
          )
        }}
      </Query>
    )
  }
}

export default Records
