import React from "react";
import { Container } from "./style";
import axios from "../../services/axios";
import { useDispatch } from "react-redux";
import * as exAct from '../../store/modules/example/actions'
import Card from "../Product/Card";
function Home() {


    return (
        <Container>
            <Card />
            

        </Container>

    );
}

export default Home;