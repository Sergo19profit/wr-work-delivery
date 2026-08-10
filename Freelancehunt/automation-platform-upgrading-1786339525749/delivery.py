```typescript
// src/app/dashboard/page.tsx
// This file represents a potential new feature or a significant upgrade to an existing dashboard page
// within the automation platform, leveraging the specified tech stack.
// It demonstrates data fetching from Supabase, state management, and UI rendering with Tailwind CSS.

import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import React from 'react';
import { Database } from '@/types/supabase'; // Assuming a types/supabase.ts generated from Supabase CLI

// Define a type for the automation tasks, matching a potential 'automation_tasks' table in Supabase
interface AutomationTask {
  id: string;
  name: string;
  description: string | null;
  status: 'pending' | 'running' | 'completed' | 'failed';
  created_at: string;
  last_run_at: string | null;
}

// Helper function to simulate a delay for demonstration purposes (e.g., slow API)
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export default async function DashboardPage() {
  const supabase = createServerComponentClient<Database>({ cookies });

  let tasks: AutomationTask[] = [];
  let error: string | null = null;
  let isLoading = true; // Managed by React's suspense boundary in a real app, but here for clarity

  try {
    // Simulate network delay for a more realistic loading experience
    // await sleep(1500); 

    // Fetch automation tasks from Supabase
    // This assumes a table named 'automation_tasks' in your Supabase instance.
    const { data, error: supabaseError } = await supabase
      .from('automation_tasks')
      .select('*')
      .order('created_at', { ascending: false });

    if (supabaseError) {
      console.error('Error fetching automation tasks:', supabaseError);
      error = 'Failed to load automation tasks. Please try again.';
    } else {
      tasks = data as AutomationTask[]; // Type assertion based on our interface
    }
  } catch (err) {
    console.error('Unexpected error during data fetch:', err);
    error = 'An unexpected error occurred. Please refresh the page.';
  } finally {
    isLoading = false; // In a real app, this would be handled by Next.js loading.tsx or Suspense
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 sm:p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Automation Dashboard</h1>
        <p className="mt-2 text-lg text-gray-600">Overview of your automated workflows and tasks.</p>
      </header>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Recent Tasks</h2>
        {isLoading ? ( // Simplified loading state for server component
          <div className="flex items-center justify-center p-8 bg-white rounded-lg shadow-sm">
            <svg className="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="ml-3 text-gray-700">Loading tasks...</span>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Error:</strong>
            <span className="block sm:inline ml-2">{error}</span>
          </div>
        ) : tasks.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow-sm text-center text-gray-600">
            <p className="text-lg">No automation tasks found. Start by creating a new workflow!</p>
            {/* In a real app, this would link to a /new-workflow page */}
            <button className="mt-4 px-6 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition-colors">
              Create New Task
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map((task) => (
              <div key={task.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{task.name}</h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">{task.description || 'No description provided.'}</p>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
                  <span>Status:</span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      task.status === 'completed' ? 'bg-green-100 text-green-800' :
                      task.status === 'running' ? 'bg-blue-100 text-blue-800' :
                      task.status === 'failed' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>Created:</span>
                  <span>{new Date(task.created_at).toLocaleDateString()}</span>
                </div>
                {task.last_run_at && (
                  <div className="flex items-center justify-between text-sm text-gray-500 mt-1">
                    <span>Last Run:</span>
                    <span>{new Date(task.last_run_at).toLocaleString()}</span>
                  </div>
                )}
                {/* Action buttons could go here */}
                <div className="mt-4 flex justify-end space-x-2">
                  <button className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-2