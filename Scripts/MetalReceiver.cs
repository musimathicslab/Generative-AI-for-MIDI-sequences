using UnityEngine;
using System;
using System.Collections.Generic;
using OscJack;

public class MetalReceiver : MonoBehaviour
{
    [Header("Strumenti")]
    public AudioSource guitarSource;
    public AudioSource bassSource;
    public AudioSource kickSource;
    public AudioSource snareSource;
    public AudioSource hihatSource;

    [Header("Stato Sblocco Strumenti")]
    public bool guitarActive = true;
    public bool bassActive = false;
    public bool drumsActive = false;

    private readonly Queue<Action> _executionQueue = new Queue<Action>();
    private float baseNote = 40f;

    // Manteniamo il server come variabile di classe per evitare che venga rimosso dalla memoria
    private OscServer _server;

    void Start()
    {
        AudioConfiguration config = AudioSettings.GetConfiguration();
        config.dspBufferSize = 256;
        AudioSettings.Reset(config);
        _server = new OscServer(5005);

        // --- CALLBACK CHITARRA ---
        _server.MessageDispatcher.AddCallback("/instrument/guitar", (string address, OscDataHandle data) => {
            if (!guitarActive) return;
            float p = data.GetElementAsFloat(0);
            float v = data.GetElementAsFloat(1);
            lock (_executionQueue) { _executionQueue.Enqueue(() => PlaySound(guitarSource, p, v)); }
        });

        // --- CALLBACK BASSO ---
        _server.MessageDispatcher.AddCallback("/instrument/bass", (string address, OscDataHandle data) => {
            if (!bassActive) return;
            float p = data.GetElementAsFloat(0);
            float v = data.GetElementAsFloat(1);
            lock (_executionQueue) { _executionQueue.Enqueue(() => PlaySound(bassSource, p, v)); }
        });

        // --- CALLBACK BATTERIA (KICK, SNARE, HIHAT) ---
        _server.MessageDispatcher.AddCallback("/instrument/drums/kick", (string address, OscDataHandle data) => {
            if (!drumsActive) return;
            lock (_executionQueue) { _executionQueue.Enqueue(() => kickSource.PlayOneShot(kickSource.clip)); }
        });

        _server.MessageDispatcher.AddCallback("/instrument/drums/snare", (string address, OscDataHandle data) => {
            if (!drumsActive) return;
            lock (_executionQueue) { _executionQueue.Enqueue(() => snareSource.PlayOneShot(snareSource.clip)); }
        });

        _server.MessageDispatcher.AddCallback("/instrument/drums/hihat", (string address, OscDataHandle data) => {
            if (!drumsActive) return;
            lock (_executionQueue) { _executionQueue.Enqueue(() => hihatSource.PlayOneShot(hihatSource.clip)); }
        });

        Debug.Log("MetalReceiver: Server OSC avviato sulla porta 5005");
    }

    // Fondamentale: Liberiamo la porta quando premi STOP in Unity
    void OnDestroy()
    {
        if (_server != null)
        {
            _server.Dispose();
            _server = null;
        }
    }
    void OnValidate()
    {
        // Forza la chitarra a essere sempre attiva nell'Inspector
        guitarActive = true;
    }

    void Update()
    {
        AudioListener.volume = 1f;
        AudioListener.pause = false;
        lock (_executionQueue)
        {
            while (_executionQueue.Count > 0) { _executionQueue.Dequeue().Invoke(); }
        }
    }

    void PlaySound(AudioSource source, float pitch, float velocity)
    {
        if (source == null || source.clip == null) return;
        if (!source.gameObject.activeInHierarchy) return;

        source.pitch = Mathf.Pow(1.05946f, pitch - baseNote);
        source.volume = velocity / 127f;
        source.PlayOneShot(source.clip);
    }

    public void AttivaStrumentoIA(string instrumentName)
    {
        switch (instrumentName)
        {
            case "ElectricBass":
            case "DoubleBass":
            case "Bass":
                bassActive = true;
                break;
            case "Drum":
            case "Drums":
                drumsActive = true;
                break;
            case "Guitar":
                guitarActive = true;
                break;
        }
    }
}
