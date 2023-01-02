import  {createGlobalStyle} from "styled-components"
import 'react-toastify/dist/ReactToastify.css'

export default createGlobalStyle`
*{
    margin: 0;
    padding: 0;
    outline: none;
    box-sizing: border-box;
}

a {
    text-decoration: none;
    color: white;
    padding-right: 10px;
    transition: all 200ms;
}
a:hover {
    color: #808080;
}

ul {
    list-style: none;
}



`;

