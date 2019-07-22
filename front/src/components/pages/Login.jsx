import React, { Component } from 'react'
import { Formik, ErrorMessage } from 'formik'
import { Icon, Layout, Tooltip } from 'antd'
import { Form, Input, SubmitButton } from '@jbuschke/formik-antd'
import gql from 'graphql-tag'
import { Mutation } from 'react-apollo'
import * as Yup from 'yup'

const { Content } = Layout

const TOKEN_AUTH = gql`
mutation TokenAuth($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
        token
    }
}
`

const SignInSchema = Yup.object().shape({
  username: Yup.string()
    .min(4, 'Too short')
    .max(50, 'Too long')
    .required('Required'),
  password: Yup.string()
    .required('Password required'),
})

export default class Login extends Component {
  render() {
    return (
      <Content
        style={{
          margin: '24px 16px',
          padding: 24,
          background: '#fff'
        }}
      >
        <Mutation
          mutation={TOKEN_AUTH}
          update={(cache, {data: {tokenAuth}}) => {
            const {token} = tokenAuth
            localStorage.setItem('token', token)
            this.props.history.push('/')
          }}
        >
          {(tokenAuth, {data}) => (
            <Formik
              initialValues={{username: '', password: ''}}
              validationSchema={SignInSchema}
              onSubmit={(values, { setSubmitting }) => {
                const {username, password} = values
                setSubmitting(false)
                tokenAuth({variables: {username, password}})
              }}
              render={({errors, status, touched, isSubmitting}) => (
                <Form>
                  <Form.Item>
                    <Input
                      prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}} />} 
                      name="username"
                      placeholder="Username"
                    />
                    <ErrorMessage name="username" />
                  </Form.Item>
                  <Form.Item>
                    <Input.Password
                      prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                      name="password"
                      placeholder="Password"
                    />
                    <ErrorMessage name="password" />
                  </Form.Item>
                  <SubmitButton>Login</SubmitButton>
                </Form>
              )}
            />
          )}
        </Mutation>
      </Content>
    )
  }
}