import React, { Component } from 'react'

import { Layout, Icon } from 'antd'

import NavRouterMenu from './components/layout/NavRouterMenu'
import Router from './Router'

import './App.css'


const { Header, Sider } = Layout

class App extends Component {
  state = {
    collapsed: false
  }

  toggleCollapsed = () => this.setState({collapsed: !this.state.collapsed})

  render() {
    return (
      <Layout>
        <Sider 
          trigger={null} 
          collapsible 
          collapsed={this.state.collapsed}
          style={{
            height: '100vh'
          }}
        >
          <div className="logo" />
          <NavRouterMenu />
        </Sider>
        <Layout>
          <Header style={{background: '#fff', padding: 0}}>
            <Icon
              className="trigger"
              type={this.state.collapsed ? 'menu-unfold': 'menu-fold'}
              onClick={this.toggleCollapsed}
            />
          </Header>
          <Router {...this.props} />
        </Layout>
      </Layout>
    )
  }
}

export default App
