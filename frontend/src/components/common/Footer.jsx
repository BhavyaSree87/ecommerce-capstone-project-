import React from 'react'

export default function Footer(){
  return (
    <footer className="bg-gray-50 border-t mt-8">
      <div className="max-w-6xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <h4 className="font-semibold mb-3">AI Fashion</h4>
          <p className="text-sm text-gray-600">Your destination for trendy fashion, personalized shopping and seamless online experience.</p>
        </div>
        <div>
          <h5 className="font-medium mb-2">Company</h5>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>About</li>
            <li>Careers</li>
            <li>Contact</li>
          </ul>
        </div>
        <div>
          <h5 className="font-medium mb-2">Help</h5>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>Customer Care</li>
            <li>Shipping</li>
            <li>Returns</li>
          </ul>
        </div>
        <div>
          <h5 className="font-medium mb-2">Follow</h5>
          <div className="flex gap-3">
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">F</div>
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">I</div>
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">T</div>
          </div>
        </div>
      </div>
      <div className="bg-white border-t">
        <div className="max-w-6xl mx-auto px-4 py-4 text-sm text-gray-500">© {new Date().getFullYear()} StyleHub. All rights reserved.</div>
      </div>
    </footer>
  )
}
