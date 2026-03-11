function Navbar() {
    return (

        <div className="w-full bg-white shadow-sm px-4 py-3 md:py-4 sticky top-0 z-0 border-b border-gray-100">

            {/* Container */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 md:gap-4">

                {/* Mobile Header Layer (Logo + Profile Picture show up here on mobile) */}
                <div className="flex items-center justify-between md:hidden">
                    <div className="text-lg font-semibold flex items-center">
                        <span className="text-xl mr-2">🌊</span> KadalVazhi
                    </div>

                    <div className="flex items-center gap-2">
                        <img
                            src="https://i.pravatar.cc/40"
                            className="w-8 h-8 rounded-full border border-gray-200"
                            alt="Profile"
                        />
                    </div>
                </div>

                {/* Controls Layer */}
                <div className="flex flex-row items-center gap-2 w-full md:w-full md:justify-end">

                    {/* Location */}
                    <input
                        type="text"
                        placeholder="Location"
                        className="border border-gray-300 px-3 py-2 rounded-lg text-sm flex-1 md:flex-none md:w-48 outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />

                    {/* Date */}
                    <input
                        type="date"
                        className="border border-gray-300 px-3 py-2 rounded-lg text-sm flex-1 md:flex-none md:w-40 outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />

                    {/* Profile on Desktop (Hidden on Mobile) */}
                    <div className="hidden md:flex items-center gap-3 ml-2 pl-4 border-l border-gray-200">
                        <img
                            src="https://i.pravatar.cc/40"
                            className="w-9 h-9 rounded-full shadow-sm border border-gray-200"
                            alt="Profile"
                        />
                        <span className="font-medium text-sm text-gray-700">
                            Nithil
                        </span>
                    </div>

                </div>

            </div>

        </div>

    )
}

export default Navbar