import axios from 'axios';

const setAuthHeader = (token) => {
    if(token) {
        axios.defaults.headers = {
            Authorization: "Bearer " + token,
            "Content-type": "Application/json"
        };
    }else{
        delete axios.defaults.headers.Authorization;
    }
};

export default setAuthHeader;