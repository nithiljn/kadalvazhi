function Sidebar() {

    return (
        <div className="h-dvh w-16 md:w-64 lg:w-80 bg-white shadow-xl rounded-r-lg flex flex-col shrink-0 transition-all duration-300 z-10 border-r border-gray-100">

            <div className="p-4 flex items-center justify-center md:justify-between h-[68px] border-b border-gray-100">
                {/* Text - hidden on smaller than md */}
                <div className="font-bold text-lg hidden md:block whitespace-nowrap overflow-hidden text-ellipsis">
                    KadalVazhi
                </div>

                {/* Hamburger */}
                <div className="cursor-pointer text-xl hover:bg-gray-100 rounded-lg h-10 w-10 flex items-center justify-center shrink-0">
                    ☰
                </div>
            </div>

            <div className="flex-1 p-3 overflow-y-auto overflow-x-hidden">
                <div className="flex items-center justify-center md:justify-start cursor-pointer hover:bg-gray-100 p-2 md:p-3 rounded-lg font-bold text-blue-600 hover:text-blue-700 bg-blue-50 transition-colors">
                    <span className="text-xl md:mr-3">+</span>
                    <span className="hidden md:block whitespace-nowrap text-sm">New Chat</span>
                </div>
            </div>

            {/*footer*/}
            <div className="p-3">
                <div className="border-t border-gray-200 pt-3 flex items-center justify-center md:justify-start font-medium text-gray-600 cursor-pointer hover:bg-gray-100 p-2 md:p-3 rounded-lg transition-colors">
                    <span className="text-xl md:mr-3">⚙️</span>
                    <span className="hidden md:block whitespace-nowrap text-sm text-center">Settings</span>
                </div>
            </div>

        </div>
    )
}

export default Sidebar