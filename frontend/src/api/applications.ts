import apiClient from './axios'

export interface Application {
  id: string
  user_id: string
  company_name: string
  role_title: string
  job_url: string | null
  location: string | null
  salary_min: number | null
  salary_max: number | null
  stage: string
  applied_date: string
  created_at: string
  updated_at: string
  notes?: Note[]
}

export interface Note {
  id: string
  application_id: string
  content: string
  created_at: string
}

export interface ApplicationParams {
  stage?: string
  search?: string
  sort_by?: string
  order?: string
}

export interface CreateApplicationData {
  company_name: string
  role_title: string
  job_url?: string
  location?: string
  salary_min?: number
  salary_max?: number
  applied_date?: string
}

export const getApplications = (params?: ApplicationParams) =>
  apiClient.get('/applications', { params }).then((r) => r.data)

export const getApplication = (id: string) =>
  apiClient.get(`/applications/${id}`).then((r) => r.data)

export const createApplication = (data: CreateApplicationData) =>
  apiClient.post('/applications', data).then((r) => r.data)

export const updateApplication = (id: string, data: Partial<CreateApplicationData>) =>
  apiClient.patch(`/applications/${id}`, data).then((r) => r.data)

export const updateStage = (id: string, stage: string) =>
  apiClient.patch(`/applications/${id}/stage`, { stage }).then((r) => r.data)

export const deleteApplication = (id: string) =>
  apiClient.delete(`/applications/${id}`)
