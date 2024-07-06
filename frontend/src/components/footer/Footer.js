import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
const { Footer } = Layout;

const FooterComponent = () => {
    return <Footer
        style={{
            textAlign: 'center',
        }}
    >
        Skibbidy Skit Planner ©{new Date().getFullYear()} Created by Hello Team
    </Footer>
}

export default FooterComponent;