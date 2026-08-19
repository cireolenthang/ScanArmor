import React, { useState } from 'react'

export default function IssueCard({issue}){
  const [open, setOpen] = useState(false)
  const sev = (issue.severity || '').toLowerCase()
  const sevClasses = sev === 'critical' ? 'bg-red-700 text-white' :
                     sev === 'high' ? 'bg-red-100 text-red-800' :
                     sev === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                     'bg-green-100 text-green-800'

  return (
    <div className="border p-3 rounded bg-white shadow-sm">
      <div className="flex justify-between items-start">
        <div>
          <div className="font-bold text-gray-800">{issue.title}</div>
          <div className="text-sm text-gray-600 mt-1">{issue.short || issue.detail.slice(0, 120)}</div>
        </div>
        <div className="ml-4 flex flex-col items-end space-y-2">
          <span className={`px-2 py-1 rounded text-xs font-semibold ${sevClasses}`}>{issue.severity}</span>
          <button aria-expanded={open} onClick={() => setOpen(v => !v)} className="text-sm text-blue-600 hover:underline">{open ? 'Hide' : 'Details'}</button>
        </div>
      </div>
      {open && (
        <div className="mt-3 text-sm text-gray-700">
          {issue.detail}
        </div>
      )}
    </div>
  )
}
