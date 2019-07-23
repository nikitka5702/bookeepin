import React, {Component, Fragment} from 'react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router'

import { Menu, Icon } from 'antd'

const { SubMenu } = Menu

class NavRouterMenu extends Component {
  render() {
    const isAuthenticated = Boolean(localStorage.getItem('token'))

    const auth =
      isAuthenticated ?
        (
          [
            <Menu.Item key="1">
              <Icon type="info-circle" />
              <span>Main</span>
              <Link to="/" />
            </Menu.Item>,
            <SubMenu 
              key="sub1"
              title={
                <span>
                  <Icon type="user" />
                  <span>Profile</span>
                </span>
              }
            >
              <Menu.Item key="2">
                <Icon type="rise" />
                <span>Incomes</span>
                <Link to='incomes' />
              </Menu.Item>
              <Menu.Item key="3">
                <Icon type="fall" />
                <span>Expenses</span>
              </Menu.Item>
              <Menu.Item key="4">
                <Icon type="pie-chart" />
                <span>Statistics</span>
              </Menu.Item>
            </SubMenu>,
            <Menu.Item key="5">
              <Icon type="logout" />
              <span>Logout</span>
              <a href="#$" onClick={e => {
                localStorage.removeItem('token')
                this.props.history.push('/')
              }} />
            </Menu.Item>
          ]
        ) : (
          [
            <Menu.Item key="1">
              <Icon type="info-circle" />
              <span>Main</span>
              <Link to="/" />
            </Menu.Item>,
            <Menu.Item key="2">
              <Icon type="login" />
              <span>Login</span>
              <Link to="login" />
            </Menu.Item>,
            <Menu.Item key="3">
              <Icon type="profile" />
              <span>Register</span>
              <Link to="reg" />
            </Menu.Item>
          ]
        )

    return (
      <Menu
        mode="inline"
        theme="dark"
        selectable={false}
      >
        {auth.map(el => el)}
      </Menu>
    )
  }
}

export default withRouter(NavRouterMenu)
