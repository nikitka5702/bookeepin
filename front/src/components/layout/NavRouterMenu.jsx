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
            <Fragment>
              <Icon type="info-circle" />
              <span>Main</span>
              <Link to="/" />
            </Fragment>,
            <Fragment>
              <Icon type="user" />
              <span>Profile</span>
              <Link to="profile" />
            </Fragment>,
            <Fragment>
              <Icon type="logout" />
              <span>Logout</span>
              <a href="#$" onClick={e => {
                localStorage.removeItem('token')
                this.props.history.push('/')
              }} />
            </Fragment>
          ]
        ) : (
          [
            <Fragment>
              <Icon type="info-circle" />
              <span>Main</span>
              <Link to="/" />
            </Fragment>,
            <Fragment>
              <Icon type="login" />
              <span>Login</span>
              <Link to="login" />
            </Fragment>,
            <Fragment>
              <Icon type="profile" />
              <span>Register</span>
              <Link to="reg" />
            </Fragment>
          ]
        )

    return (
      <Menu
        mode="inline"
        theme="dark"
        selectable={false}
      >
        {auth.map((el, idx) => <Menu.Item key={idx}>{el}</Menu.Item>)}
      </Menu>
    )
  }
}

export default withRouter(NavRouterMenu)
