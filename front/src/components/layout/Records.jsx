import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { Formik, ErrroMessage } from 'formik'
import { Layout, Pagination, Spin, Row, Col, Alert, Menu } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

import lookup from '../../helper'

class Records extends Component {
  static propTypes = {
    accountId: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    qname: PropTypes.string.isRequired,
    query: PropTypes.object.isRequired,
    fields: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
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
    const { accountId, name, qname, query, fields, mutations } = this.props
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
              <Row type="flex" justify="center" align="middle" style={{height: '85%'}}>
              </Row>
              <Row type="flex" justify="center" align="middle" style={{height: '10%'}}>
                <Pagination
                  showSizeChanger
                  current={page}
                  defaultPageSize={pageSize}
                  onShowSizeChange={(_, pageSize) => this.setState({pageSize})}
                  onChange={page => this.setState({page})}
                  total={data[qname].total}
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
