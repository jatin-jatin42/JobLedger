import apiClient from './axios'

export const getNotes = (applicationId: string) =>
  apiClient.get(`/applications/${applicationId}/notes`).then((r) => r.data)

export const createNote = (applicationId: string, content: string) =>
  apiClient.post(`/applications/${applicationId}/notes`, { content }).then((r) => r.data)

export const deleteNote = (applicationId: string, noteId: string) =>
  apiClient.delete(`/applications/${applicationId}/notes/${noteId}`)
