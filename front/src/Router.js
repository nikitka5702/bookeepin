import React from 'react'
import {Route, Switch} from 'react-router-dom'

import Index from './components/pages/Index'
import Login from './components/pages/Login'
import Register from './components/pages/Register'
import Incomes from './components/pages/Incomes'

const Router = props => {
  return (
    <Switch>
      <Route exact path='/' component={Index}/>
      <Route path='/login' component={Login}/>
      <Route path='/reg' component={Register}/>
      <Route path='/incomes' component={Incomes} /> 
    </Switch>
  )
}

export default Router
