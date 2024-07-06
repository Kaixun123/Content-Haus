import React, { useState, useEffect } from 'react';
import { Layout, Menu } from 'antd';
import { Grid } from 'antd';
import { Dropdown, Button } from 'antd';
import { MenuOutlined } from '@ant-design/icons';
import './Navbar.css';
import { Link, useLocation } from 'react-router-dom';
const { useBreakpoint } = Grid;
const { Header } = Layout;

const getItems = () => {
    const commonItems = [
        { key: '1', label: 'Home', route: `/home` },
        { key: '2', label: 'Landing', route: `/landing` },
    ];

    return commonItems;
};

const Navbar = () => {
    const items = getItems();
    const screens = useBreakpoint();
    const [selectedKey, setSelectedKey] = useState([]);
    const location = useLocation();

    const dropdownMenu = (
        <Menu
            theme="dark"
            mode="vertical"
            defaultSelectedKeys={[]}
            selectedKeys={selectedKey}
        >
            {items.map(item => {
                return (
                    <Menu.Item key={item.key}>
                        <Link to={item.route}>
                            {item.label}
                        </Link>
                    </Menu.Item>
                );
            })}
        </Menu>
    );

    useEffect(() => {
        const currentPath = location.pathname;
        const matchingItem = items.find(item => item.route === currentPath);
        if (matchingItem) {
            setSelectedKey([matchingItem.key]);
        } else {
            setSelectedKey([]);
        }
    }, [location]);

    return (
        <Layout>
            <Header
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }}
            >
                {/* <Link to="/home">
                    <Logo className='logo' />
                </Link> */}
                {screens.xs ? (
                    <Dropdown menu={dropdownMenu}>
                        <Button
                            className="menu-button"
                            type="primary"
                            icon={<MenuOutlined />}
                        />
                    </Dropdown>
                ) : (
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={[]}
                        selectedKeys={selectedKey}
                        style={{ flex: 1 }}
                    >
                        {items.map(item => {
                            return (
                                <Menu.Item key={item.key}>
                                    <Link to={item.route}>
                                        {item.label}
                                    </Link>
                                </Menu.Item>
                            );
                        })}
                    </Menu>
                )}
                {/* <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', right: 10 }}>
                    <Profile />
                </div> */}
            </Header>
        </Layout>
    );
}

export default Navbar;