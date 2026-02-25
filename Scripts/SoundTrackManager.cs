using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class SoundTrackManager : MonoBehaviour
{
    // AI Connection 
    public MetalReceiver metalReceiver;

    // Start is called before the first frame update
    public AudioSource bass;
    public AudioSource guitar;
    public AudioSource drum;

    //MAIN CANVAS
    public GameObject CARDUI;
    
    //IMAGE
    public GameObject bass_image;
    public GameObject guitar_image;
    public GameObject drum_image;

    public GraphicRaycaster raycaster;
    public EventSystem eventSystem;

    private bool isRotating=false;
    private float RotationDuration = 1f;

    private bool hasPickedBass = false;
    private bool hasPickedDrums = false;

    //SISTEMA CHE UTILIZZA L'AI PER LA MUSICA
    [System.Obsolete]
    void Start()
    {
        if (metalReceiver == null) metalReceiver = FindObjectOfType<MetalReceiver>();

        // 1. INIZIO: Assicuriamoci che suoni SOLO la chitarra
        // (Assumi che Python stia mandando tutto, ma MetalReceiver ha guitarActive=true e il resto false)

        // Setup Audio Unity (opzionale se usi solo Python, ma utile per backup)
        guitar.volume = 1f;
        bass.volume = 0f;
        drum.volume = 0f;

        // Nascondi tutte le immagini all'inizio
        resetImages();
    }

    // --- CHECKPOINT 1: LA PRIMA SCELTA (Basso vs Batteria) ---
    public void CheckPoint1()
    {
        resetImages();

        // Attiviamo le due opzioni principali
        bass_image.SetActive(true);
        drum_image.SetActive(true);

        CARDUI.SetActive(true);
        FightManager.Instance.cardChosing = true;
        Time.timeScale = 0f; // Metti in pausa il gioco durante la scelta
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
    }

    // --- CHECKPOINT 2: LA SCELTA OBBLIGATA (Quello che manca) ---
    public void CheckPoint2()
    {
        resetImages();

        // Se hai già il basso, mostra SOLO la batteria a DESTRA (Butt2)
        if (hasPickedBass && !hasPickedDrums)
        { 
            bass_image.transform.parent.gameObject.SetActive(false);
            drum_image.transform.parent.gameObject.SetActive(true);
            drum_image.SetActive(true);
        }
        // Se hai già la batteria, mostra SOLO il basso a SINISTRA (Butt1)
        else if (hasPickedDrums && !hasPickedBass)
        {
            drum_image.transform.parent.gameObject.SetActive(false);
            bass_image.transform.parent.gameObject.SetActive(true);
            bass_image.SetActive(true);
        }

        CARDUI.SetActive(true);
        FightManager.Instance.cardChosing = true;
        Time.timeScale = 0f;
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
    }

    void Update()
    {
        if (FightManager.Instance.cardChosing && Input.GetMouseButtonDown(0))
        {
            PointerEventData pointerData = new PointerEventData(eventSystem);
            pointerData.position = Input.mousePosition;

            List<RaycastResult> results = new List<RaycastResult>();
            raycaster.Raycast(pointerData, results);

            foreach (RaycastResult result in results)
            {
                if (result.gameObject.CompareTag("CLICKABLE"))
                {
                    string chosenInstrument = "";

                    if (result.gameObject.name.Equals("Butt1"))
                    {
                        chosenInstrument = CheckActive("L");
                    }
                    else
                    {
                        chosenInstrument = CheckActive("R");
                    }

                    // Se l'utente ha cliccato un pulsante vuoto (succede nel CP2), non fare nulla
                    if (chosenInstrument != "")
                    {
                        activateTrack(chosenInstrument);
                        CloseCardUI();
                    }
                }
            }
        }
    }

    public void activateTrack(string instrument)
    {
        // 1. Logica IA
        if (metalReceiver != null)
        {
            metalReceiver.AttivaStrumentoIA(instrument);
        }

        // 2. Logica Unity & Statistiche
        // Nota: Qui usiamo i nomi ESATTI dei GameObjects delle immagini
        switch (instrument)
        {
            case "ElectricBass": // Assicurati che il GameObject si chiami così
            case "Bass":
                hasPickedBass = true; // Memorizziamo la scelta!
                FightManager.Instance.UpdateGameStat("dashcd", -2f);
                if (bass != null) bass.volume = 1f;
                break;

            case "Drum": // Assicurati che il GameObject si chiami così
            case "Drums":
                hasPickedDrums = true; // Memorizziamo la scelta!
                FightManager.Instance.UpdateGameStat("damage", 10f);
                if (drum != null) drum.volume = 1f;
                break;
        }
    }

    void CloseCardUI()
    {
        Time.timeScale = 1f;
        CARDUI.SetActive(false);
        FightManager.Instance.cardChosing = false;
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;
    }

    public void resetImages()
    {
        // Disattiva tutto (incluso violino e tamburello se erano rimasti)
        // Assicurati che questo codice raggiunga tutti i figli corretti
        if (drum_image != null && drum_image.transform.parent != null)
        {
            foreach (Transform g in drum_image.transform.parent) g.gameObject.SetActive(false);
        }
        if (tambourine_image != null && tambourine_image.transform.parent != null)
        {
            foreach (Transform g in tambourine_image.transform.parent) g.gameObject.SetActive(false);
        }
        // Aggiungi qui i riferimenti ai parenti delle altre immagini se sono su pannelli diversi
    }

    public string CheckActive(string side)
    {
        string chosen_instr = "";

        // Se clicco il lato L (Butt1), controllo solo i figli di quel parent
        if (side.Equals("L"))
        {
            // Cerca tra i figli del parent di bass_image (Butt1)
            foreach (Transform g in bass_image.transform.parent)
            {
                if (g.gameObject.activeSelf)
                {
                    chosen_instr = g.name;
                    break;
                }
            }
        }
        else if (side.Equals("R"))
        {
            // Cerca tra i figli del parent di drum_image (Butt2)
            foreach (Transform g in drum_image.transform.parent)
            {
                if (g.gameObject.activeSelf)
                {
                    chosen_instr = g.name;
                    break;
                }
            }
        }

        return chosen_instr;
    }
