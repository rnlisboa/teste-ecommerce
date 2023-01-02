import React, { useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from "../../services/axios";
import { useDispatch } from "react-redux";
import * as actions from '../../store/modules/auth/actions'
import { toast } from 'react-toastify'
import { isEmail } from 'validator'
import { get } from 'lodash'

function Login(props) {
  const dispatch = useDispatch()
  const prevPath = (props, 'location.state.prevPath', '/')
  const [firstname, setFirstame] = useState([])
  const [username, setUsername] = useState([])
  const [email, setEmail] = useState([])
  const [password, setPassword] = useState([])

  async function handleSubmitRegister(e) {
    e.preventDefault()
    let formErrors = false

    if (firstname.length <= 3 || firstname.length > 255) {
      formErrors = true;
      toast.error('Nome deve ter entre 4 e 249 caracteres.')
    }
    if (username.length <= 3 || username.length > 255) {
      formErrors = true;
      toast.error('Nome de usuário deve ter entre 4 e 249 caracteres.')
    }
    if (password.length < 8 || password.length > 50) {
      formErrors = true;
      toast.error('Nome deve ter entre 8 e 50 caracteres.')
    }
    if (!isEmail(email)) {
      formErrors = true;
      toast.error('E-mail inválido.')
    }

    if (formErrors) return

    try {
      await axios.post('/api/users/register/', {
        firstname, username, password, email
      })
      toast.success('Usuário registrado com sucesso.')

    } catch (e) {

      const errors = get(e, 'response.data.errors', [])

      if (errors.email) {
        toast.error('E-mail já cadastrado.')
      }
      if (errors.username) {
        toast.error('Nome de usuário já está em uso.')
      }

    }
  }

  async function handleSubmitLogin(e) {
    e.preventDefault()
    
    
    dispatch(actions.loginRequest({username, password, prevPath}))
    
  }
  return (
    <Container className="mt-5">
      <Row >
        <Col className="col-lg">
          <h1>Login </h1>

          <Form onSubmit={handleSubmitLogin}>
            <Form.Group className="mb-3">
              <Form.Label>Usuário</Form.Label>
              <Form.Control type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Nome de usuário" />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Senha</Form.Label>
              <Form.Control type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Sua senha" />
            </Form.Group>

            <Button variant="primary" type="submit">
              Entrar
            </Button>
          </Form>
        </Col>
        <Col className="col-lg">

          <h1>Cadastro </h1>
          <Form onSubmit={handleSubmitRegister}>
            <Form.Group className="mb-3">
              <Form.Label>Nome</Form.Label>
              <Form.Control type="text" value={firstname} onChange={e => setFirstame(e.target.value)} placeholder="Seu primeiro nome" />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Usuário</Form.Label>
              <Form.Control type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Nome de usuário" />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>E-mail</Form.Label>
              <Form.Control type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Seu melhor email" />
            </Form.Group>


            <Form.Group className="mb-3">
              <Form.Label>Senha</Form.Label>
              <Form.Control type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Sua senha" />
            </Form.Group>

            <Button variant="primary" type="submit">
              Cadastrar
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>




  );
}

export default Login;