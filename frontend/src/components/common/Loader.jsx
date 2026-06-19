import React from 'react'

export default function Loader(){
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="inline-flex h-16 w-16 items-center justify-center rounded-full border-4 border-primary border-t-transparent animate-spin" />
    </div>
  )
}
