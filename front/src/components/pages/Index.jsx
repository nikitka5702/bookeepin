import React, {Component} from 'react'
import { Layout } from 'antd'

const { Content } = Layout

export default class Index extends Component {
  render() {
    return (
      <Content
        style={{
          margin: '24px 16px',
          padding: 24,
          background: '#fff'
        }}
      >
        Hello
      </Content>
    )
  }
}