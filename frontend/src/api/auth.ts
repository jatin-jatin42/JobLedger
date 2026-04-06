import apiClient from './axios'

export const register = (data: { email: string; password: string; full_name: string }) =>
  apiClient.post('/auth/register', data).then((r) => r.data)

export const login = (data: { email: string; password: string }) =>
  apiClient.post('/auth/login', data).then((r) => r.data)

export const getMe = () =>
  apiClient.get('/auth/me').then((r) => r.data)
