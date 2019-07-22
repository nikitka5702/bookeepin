import React, { Component } from 'react'
import { Formik, ErrroMessage } from 'formik'
import { Layout, Pagination } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Query, Mutation } from 'react-apollo'
import * as Yup from 'yup'

const { Content } = Layout

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
        <Pagination
          showSizeChanger
          onShowSizeChange={this.setPageSize}
          onChange={this.logData}
          defaultCurrent={this.state.page}
          total={250}
        />
      </Content>
    )
  }
}

export default Incomes
