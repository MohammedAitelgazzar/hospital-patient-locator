package com.app.controllers;

import com.app.entities.Localisation;
import com.app.services.LocalisationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@RequestMapping("/api/localisations")
public class LocalisationController {

    @Autowired
    private LocalisationService localisationService;

    @PostMapping
    public ResponseEntity<Localisation> createLocalisation(@RequestBody Localisation localisation) {
        try {
            Localisation savedLocalisation = localisationService.saveLocalisation(localisation);
            return ResponseEntity.ok(savedLocalisation);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Localisation>> getAllLocalisations() {
        try {
            List<Localisation> localisations = localisationService.getAllLocalisations();
            return ResponseEntity.ok(localisations);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Localisation> getLocalisationById(@PathVariable String id) {
        try {
            return localisationService.getLocalisationById(id)
                    .map(ResponseEntity::ok)
                    .orElse(ResponseEntity.notFound().build());
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteLocalisation(@PathVariable String id) {
        try {
            localisationService.deleteLocalisation(id);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
} 