import { Routes, Route } from "react-router-dom";
import Navbar from "../components/navbar/Navbar";
import Footer from "../components/footer/Footer";
import {
    PUBLIC_ROUTE_MAPS,
} from "./RouterMapper";

export const AppRouter = () => {
    const renderRoutes = (routes, prefix="") => {
        return routes.map((route, index) => (
            <Route 
                key={index}
                path={`${prefix}${route.path}`}
                element={
                    <>
                        <Navbar />
                            {route.element}
                        <Footer />
                    </>
                }
            />
        ));
    }

    return (
        <Routes>
            {renderRoutes(PUBLIC_ROUTE_MAPS, "")}
        </Routes>
    );
}