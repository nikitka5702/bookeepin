import React from 'react'
import { Layout, Spin, Row, Alert, Menu } from 'antd'
import { Query } from 'react-apollo'
import PropTypes from 'prop-types'

const { Content } = Layout

const AccountMenu = props => {
  const { query, menuSelect, children } = props

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
            query={query}
            pollInterval={10000}
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
                  onClick={({ key }) => menuSelect(Number.parseInt(key))}
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
          {children}
        </Content>
      </Layout>
    </Content>
  )
}

AccountMenu.propTypes = {
  query: PropTypes.object.isRequired,
  menuSelect: PropTypes.func.isRequired
}

export default AccountMenu
