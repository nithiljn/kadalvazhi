import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [location, setlocation] = useState("")

  return (
    <>
      <div className=' min-h-screen bg-gradient-to-b from-blue-50 to-blue-100 p-8'>
        <div className=' max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8'>
          <h1 className='text-4xl font-bold text-[--color-ocean-blue] mb-2'>🎣 KadalVazhi</h1>
          <p className='text-gray-600 mb-8'>கடல்வழி - Smart Fishing Assistant</p>
          <div className='mb-6'>
            <label className='block text-gray-700 font-semibold mb-2'>📍 Location:</label>
            <input type='text' value={location} onChange={(e) => setlocation(e.target.value)} className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-ocean-blue]' placeholder='Enter city name...' />
          </div>
          <div className='bg-blue-50 p-4 rounded-lg border-l-4 border-[--color-ocean-blue]'>
            <p className='text-lg'>✅ You entered: <strong className='text-[--color-ocean-blue]'>{location}</strong></p>
            <p className='text-sm text-gray-600 mt-2'>Try changing the location above and see it update here instantly!</p>
          </div>
        </div>
      </div>
    </>
  )
}

export default App