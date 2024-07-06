import React from 'react';

function Navbar(){
    return(
    <nav className="flex items-center justify-between flex-wrap bg-white-500 p-6">
        <div className="flex items-center flex-shrink-0 mr-6">
            <a href="/" className="flex" >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-collection-play-fill h-8 w-8 mr-2" viewBox="0 0 16 16"><path d="M2.5 3.5a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1zm2-2a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1zM0 13a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 16 13V6a1.5 1.5 0 0 0-1.5-1.5h-13A1.5 1.5 0 0 0 0 6zm6.258-6.437a.5.5 0 0 1 .507.013l4 2.5a.5.5 0 0 1 0 .848l-4 2.5A.5.5 0 0 1 6 12V7a.5.5 0 0 1 .258-.437"/></svg>
                <span className="font-semibold text-xl tracking-tight">Content-Haus</span>
            </a>
        </div>
        <div className="block lg:hidden">
            <button class="flex items-center px-3 py-2 border rounded text-black-200 border-teal-400 hover:text-white hover:border-white">
            <svg className="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
            </button>
        </div>
        <div className="w-full block flex flex-row-reverse lg:flex lg:items-center lg:w-auto">
            <div className="text-sm lg:flex-grow">
            <a href="/" className="block mt-4 lg:inline-block lg:mt-0 text-black-300 hover:text-blue mr-8">
                Home
            </a>
            <a href="/editor" className="block mt-4 lg:inline-block lg:mt-0 text-black-300 hover:text-blue mr-8">
                Upload Videos
            </a>
            <a href="#responsive-header" className="block mt-4 lg:inline-block lg:mt-0 text-black-300 hover:text-blue">
                About Us
            </a>
            </div>
        </div>
    </nav>
    );
}

export default Navbar