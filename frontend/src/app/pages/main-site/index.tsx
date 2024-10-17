import React from "react";
import {Header} from "@/app/pages/main-site/index.styles";
import Transactions from "@/app/components/transactions";

const MainSite: React.FC = () => {
    return (
        <div>
            <Header><h1>Welcome to RATTM&apos;s CO2 Calculator!</h1></Header>
            <Transactions/>
        </div>
    );
};

export default MainSite;
