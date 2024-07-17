const express = require('express');
const multer = require('multer');
const cors = require('cors');
const OpenAI = require('openai');
const fs = require('fs');
const { spawn } = require('child_process');
require('dotenv').config();

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.static('.')); // Serve static files from current directory

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// function encodeImage(imagePath) {
//   return new Promise((resolve, reject) => {
//       fs.readFile(imagePath, (err, data) => {
//           if (err) reject(err);
//           else resolve(data.toString('base64'));
//       });
//   });
// }

app.post('/analyze', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  try {
    const image = fs.createReadStream(req.file.path);
    
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Analyze this image and suggest musical elements based on it. Include a theme, mood, potential instruments, and a brief description of the visual elements." },
            { type: "image_url", image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(req.file.path).toString('base64')}` } },
          ],
        },
      ],
    });

    const analysis = response.choices[0].message.content;
    console.log(analysis)

    // Extract theme and mood from the analysis
    // This is a simplification. You might need more sophisticated parsing.
    const theme = analysis.match(/theme:?(.+)/i)?.[1].trim() || "nature";
    const mood = analysis.match(/mood:?(.+)/i)?.[1].trim() || "calm";

    // Call Python script to generate music
    const pythonProcess = spawn('python', ['music_generation.py', JSON.stringify({ theme, mood })]);

    let pythonResponse = '';
    pythonProcess.stdout.on('data', (data) => {
      pythonResponse += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        return res.status(500).json({ error: 'Failed to generate music' });
      }

      const musicResult = JSON.parse(pythonResponse);
      if (musicResult.error) {
        return res.status(500).json({ error: musicResult.error });
      }

      res.json({
        analysis: analysis,
        musicPath: musicResult.output,
        lyrics: musicResult.lyrics
      });
    });

    // Clean up the uploaded file
    fs.unlinkSync(req.file.path);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('An error occurred while processing the image.');
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
