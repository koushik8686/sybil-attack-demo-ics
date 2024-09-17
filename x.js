const mongoose = require('mongoose');

// Define the poll schema
const pollSchema = new mongoose.Schema({
    question: { type: String, required: true },
    yes: { type: Number, default: 0 },
    no: { type: Number, default: 0 }
});

// Create the Poll model
const Poll = mongoose.model('Poll', pollSchema);

// Connect to the MongoDB database
mongoose.connect('mongodb://127.0.0.1:27017/ics', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('MongoDB connected');

  // Create a new document
  const newPoll = new Poll({
    question: 'Do you like this app?',
    yes: 0,
    no: 0
  });

  // Save the new poll document
  newPoll.save()
    .then(poll => {
      console.log('Poll created:', poll);
      mongoose.connection.close();  // Close the connection after saving
    })
    .catch(err => console.error('Error creating poll:', err));

}).catch(err => console.error('MongoDB connection error:', err));
