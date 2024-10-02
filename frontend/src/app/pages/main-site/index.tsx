import React from "react";
import {Header} from "@/app/pages/main-site/index.styles";
import Transactions from "@/app/components/transactions";

const MainSite: React.FC = () => {
    return (
        <div>
            <Header><h1>we are rattm yeehaw</h1></Header>
            <Transactions/>
        </div>
    );
};

export default MainSite;
