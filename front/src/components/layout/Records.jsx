import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { Formik, ErrroMessage } from 'formik'
import { Pagination, Spin, Row, Col, Alert, Table, Button, Icon } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query } from 'react-apollo'
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
    modals: PropTypes.exact({
      add: PropTypes.element.isRequired,
      edit: PropTypes.element.isRequired,
      delete: PropTypes.element.isRequired
    }).isRequired
  }

  state = {
    selectedRowKeys: [],
    page: 1,
    pageSize: 10
  }

  onSelectChange = selectedRowKeys => this.setState({selectedRowKeys})

  render() {
    const { accountId, name, qName, qObjects, query, fields, columns, modals } = this.props
    const { selectedRowKeys, page, pageSize } = this.state

    const controls = {edit: modals.edit}
    const rowSelection = {
      selectedRowKeys,
      onChange: this.onSelectChange
    }

    const hasSelected = selectedRowKeys.length > 0

    return (
      <Query
        query={query}
        variables={{accountId: accountId, first: pageSize, skip: (page - 1) * pageSize}}
        pollInterval={10000}
      >
        {({ loading, error, data, refetch }) => {
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
              <Row type="flex" justify="start" align="middle" style={{height: '10%'}}>
                <Button.Group>
                  <Button type="primary" icon="plus">
                    Add
                  </Button>
                  <Button type="danger" disabled={!hasSelected}>
                    Delete selected
                    <Icon type="delete" />
                  </Button>
                </Button.Group>
              </Row>
              <Row type="flex" justify="center" align="top" style={{height: '75%', width: '100%'}}>
                <Table
                  style={{width: '100%'}}
                  rowSelection={rowSelection}
                  columns={columns}
                  pagination={false}
                  scroll={{
                    y: Math.floor(document.documentElement.clientHeight * .54)
                  }}
                  dataSource={data[qName][qObjects].map((value, i) => {
                    let o = {...controls}
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
