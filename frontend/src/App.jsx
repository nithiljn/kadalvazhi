import Sidebar from './components/Sidebar'
import MainContent from './components/MainContent'
import Navbar from './components/Navbar'
function App() {

  return (
    <div className="h-dvh w-full flex bg-gray-100">

      <Sidebar />

      <div className="flex-1 overflow-y-auto">

        <Navbar />

      </div>

    </div>
  )

}
export default App