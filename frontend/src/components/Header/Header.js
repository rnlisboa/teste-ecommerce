import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import axios from '../../services/axios';
import * as act from '../../store/modules/auth/actions'
import history from '../../services/history'
function Header() {
    const isAdmin = useSelector(state => state.auth.isAdmin)
    const isLoggedIn = useSelector(state => state.auth.isLoggedIn);
    const dispatch = useDispatch()
    function handleLogout(e) {
        e.preventDefault()
        dispatch(act.loginFailure())
        
        history.push('/')

    }
    return (
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Container>
                <Navbar.Brand >
                    <Link to='/'>E-Commerce</Link>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">


                    </Nav>
                    <Nav>

                        <Link to='/'>
                            Home
                        </Link>




                        {
                            isLoggedIn && !isAdmin ? (

                                <Link to='/cart'>
                                    Carrinho
                                </Link>
                            ) : (
                                <Link to='/dashboard'>
                                    Dashboard
                                </Link>
                            )
                        }



                        {
                            isLoggedIn ? (
                                <Link to="" onClick={handleLogout}>
                                    Sair
                                </Link>
                            ) : (

                                <Link to='/login'>
                                    Entrar
                                </Link>
                            )
                        }


                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;