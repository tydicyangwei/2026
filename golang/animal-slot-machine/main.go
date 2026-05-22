package main

import (
	"crypto/rand"
	"encoding/json"
	"errors"
	"log"
	"math/big"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

type Animal struct {
	ID         string `json:"id"`
	Name       string `json:"name"`
	Multiplier int    `json:"multiplier"`
	Weight     int    `json:"weight"`
	Color      string `json:"color"`
	Icon       string `json:"icon"`
}

type SpinRequest struct {
	Bet      int    `json:"bet"`
	AnimalID string `json:"animalId"`
}

type SpinResponse struct {
	Result   Animal `json:"result"`
	Selected Animal `json:"selected"`
	Bet      int    `json:"bet"`
	Win      int    `json:"win"`
	Hit      bool   `json:"hit"`
	Time     string `json:"time"`
}

var animals = []Animal{
	{ID: "elephant", Name: "大象", Multiplier: 3, Weight: 24, Color: "#4f8fbf", Icon: "/assets/elephant.svg"},
	{ID: "eagle", Name: "老鹰", Multiplier: 5, Weight: 18, Color: "#b36a38", Icon: "/assets/eagle.svg"},
	{ID: "panda", Name: "熊猫", Multiplier: 8, Weight: 13, Color: "#2e3036", Icon: "/assets/panda.svg"},
	{ID: "lion", Name: "狮子", Multiplier: 12, Weight: 9, Color: "#d5962f", Icon: "/assets/lion.svg"},
	{ID: "fox", Name: "狐狸", Multiplier: 18, Weight: 6, Color: "#d86b35", Icon: "/assets/fox.svg"},
	{ID: "rabbit", Name: "兔子", Multiplier: 25, Weight: 4, Color: "#9b77c9", Icon: "/assets/rabbit.svg"},
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/animals", animalsHandler)
	mux.HandleFunc("/api/spin", spinHandler)
	mux.Handle("/", spaHandler("frontend/dist"))

	addr := ":" + getenv("PORT", "8080")
	log.Printf("animal slot machine started: http://localhost%s", addr)

	if err := http.ListenAndServe(addr, withSecurityHeaders(mux)); err != nil {
		log.Fatal(err)
	}
}

func animalsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	writeJSON(w, http.StatusOK, animals)
}

func spinHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req SpinRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid JSON body", http.StatusBadRequest)
		return
	}
	if req.Bet <= 0 {
		http.Error(w, "bet must be greater than 0", http.StatusBadRequest)
		return
	}
	if req.Bet > 1000 {
		http.Error(w, "bet must not exceed 1000", http.StatusBadRequest)
		return
	}
	selected, ok := findAnimal(strings.TrimSpace(req.AnimalID))
	if !ok {
		http.Error(w, "animalId is required and must match an animal", http.StatusBadRequest)
		return
	}

	result, err := weightedAnimal(animals)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	hit := selected.ID == result.ID
	win := 0
	if hit {
		win = req.Bet * result.Multiplier
	}

	writeJSON(w, http.StatusOK, SpinResponse{
		Result:   result,
		Selected: selected,
		Bet:      req.Bet,
		Win:      win,
		Hit:      hit,
		Time:     time.Now().Format(time.RFC3339),
	})
}

func findAnimal(id string) (Animal, bool) {
	for _, item := range animals {
		if item.ID == id {
			return item, true
		}
	}
	return Animal{}, false
}

func weightedAnimal(items []Animal) (Animal, error) {
	total := 0
	for _, item := range items {
		if item.Weight > 0 {
			total += item.Weight
		}
	}
	if total <= 0 {
		return Animal{}, errors.New("animal prize table is empty")
	}

	n, err := rand.Int(rand.Reader, big.NewInt(int64(total)))
	if err != nil {
		return Animal{}, err
	}

	pick := int(n.Int64())
	for _, item := range items {
		if item.Weight <= 0 {
			continue
		}
		if pick < item.Weight {
			return item, nil
		}
		pick -= item.Weight
	}

	return items[len(items)-1], nil
}

func spaHandler(root string) http.Handler {
	fileServer := http.FileServer(http.Dir(root))

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cleanPath := path.Clean(r.URL.Path)
		if cleanPath == "." || cleanPath == "/" {
			fileServer.ServeHTTP(w, r)
			return
		}

		target := filepath.Join(root, filepath.FromSlash(strings.TrimPrefix(cleanPath, "/")))
		if info, err := os.Stat(target); err == nil && !info.IsDir() {
			fileServer.ServeHTTP(w, r)
			return
		}

		http.ServeFile(w, r, filepath.Join(root, "index.html"))
	})
}

func withSecurityHeaders(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Referrer-Policy", "same-origin")
		next.ServeHTTP(w, r)
	})
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil {
		log.Printf("write JSON response: %v", err)
	}
}

func getenv(key, fallback string) string {
	value := strings.TrimSpace(os.Getenv(key))
	if value == "" {
		return fallback
	}
	if _, err := strconv.Atoi(value); err != nil {
		return fallback
	}
	return value
}
