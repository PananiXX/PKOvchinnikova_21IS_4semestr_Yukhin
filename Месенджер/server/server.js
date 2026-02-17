const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');

// Создаем Express приложение
const app = express();
const server = http.createServer(app);

// Настройка CORS для Socket.io
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    credentials: true
  }
});

// Middleware
app.use(cors({
  origin: "http://localhost:3000",
  credentials: true
}));
app.use(express.json());

// Проверка работы сервера
app.get('/', (req, res) => {
  res.json({ message: 'Yapp-Up Messenger API работает!' });
});

// API для пользователей
app.get('/api/users', (req, res) => {
  res.json([
    { id: 1, username: 'alex', online: true },
    { id: 2, username: 'maria', online: false },
    { id: 3, username: 'ivan', online: true }
  ]);
});

// Хранилище активных пользователей
const onlineUsers = new Map();

// WebSocket события
io.on('connection', (socket) => {
  console.log(`✅ Новое соединение: ${socket.id} - server.js:44`);

  // Пользователь заходит онлайн
  socket.on('user-online', (userId) => {
    onlineUsers.set(socket.id, userId);
    console.log(`🟢 Пользователь ${userId} онлайн - server.js:49`);
    
    // Уведомляем других пользователей
    socket.broadcast.emit('user-status-changed', {
      userId,
      status: 'online'
    });
  });

  // Отправка сообщения
  socket.on('send-message', (messageData) => {
    console.log('📨 Новое сообщение: - server.js:60', messageData);
    
    // Отправляем сообщение получателю
    socket.broadcast.emit('receive-message', {
      ...messageData,
      id: Date.now(),
      timestamp: new Date().toISOString()
    });
    
    // Подтверждение отправителю
    socket.emit('message-sent', { success: true, messageId: Date.now() });
  });

  // Отключение пользователя
  socket.on('disconnect', () => {
    const userId = onlineUsers.get(socket.id);
    if (userId) {
      onlineUsers.delete(socket.id);
      console.log(`🔴 Пользователь ${userId} отключился - server.js:78`);
      
      // Уведомляем других пользователей
      socket.broadcast.emit('user-status-changed', {
        userId,
        status: 'offline'
      });
    }
  });
});

// Запуск сервера
const PORT = 5000;
server.listen(PORT, () => {
  console.log(`🚀 Сервер запущен на порту ${PORT} - server.js:92`);
  console.log(`🌐 Доступен по адресу: http://localhost:${PORT} - server.js:93`);
});
