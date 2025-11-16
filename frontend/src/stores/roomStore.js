import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '@/services/apiService'

export const useRoomStore = defineStore('room', () => {
    // State
    const rooms = ref([])
    const roomTypes = ref([])
    const floors = ref([])
    const currentRoom = ref(null)
    const loading = ref(false)
    const error = ref(null)

    // Getters
    const availableRooms = computed(() => {
        return rooms.value.filter(room => room.available)
    })

    const roomCount = computed(() => rooms.value.length)

    // Actions
    const getRoomById = async (id) => {
        loading.value = true
        error.value = null
        try {
            currentRoom.value = await apiFetch(`/api/rooms/${id}/`)
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const addRoom = async (roomData) => {
        loading.value = true
        error.value = null
        try {
            const response = await fetch('/api/rooms/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(roomData)
            })
            const newRoom = await response.json()
            rooms.value.push(newRoom)
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const updateRoom = async (id, roomData) => {
        loading.value = true
        error.value = null
        try {
            const response = await fetch(`/api/rooms/${id}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(roomData)
            })
            const updatedRoom = await response.json()
            const index = rooms.value.findIndex(r => r.id === id)
            if (index !== -1) {
                rooms.value[index] = updatedRoom
            }
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const deleteRoom = async (id) => {
        loading.value = true
        error.value = null
        try {
            await fetch(`/api/rooms/${id}`, { method: 'DELETE' })
            rooms.value = rooms.value.filter(r => r.id !== id)
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const fetchRoomTypes = async () => {
        loading.value = true
        error.value = null
        try {
            roomTypes.value = await apiFetch('/api/room-types/')
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const fetchFloors = async () => {
        loading.value = true
        error.value = null
        try {
            floors.value = await apiFetch('/api/floors/')
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

     const fetchRooms = async () => {
        loading.value = true
        error.value = null
        try {
            rooms.value = await apiFetch('/api/rooms/')
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }


    return {
        rooms,
        currentRoom,
        loading,
        error,
        availableRooms,
        roomCount,
        roomTypes,
        floors,
        fetchRooms,
        getRoomById,
        addRoom,
        updateRoom,
        deleteRoom,
        fetchRoomTypes,
        fetchFloors
    }
})