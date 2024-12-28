package com.app.services;

import com.app.entities.Localisation;
import com.app.repositories.LocatlisationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LocalisationService {

    @Autowired
    private LocatlisationRepository localisationRepository;

    public Localisation saveLocalisation(Localisation localisation) {
        return localisationRepository.save(localisation);
    }

    public Optional<Localisation> getLastLocalisation() {
        return localisationRepository.findTopByOrderByCreatedAtDesc();

    }
    public List<Localisation> getAllLocalisations() {
        return localisationRepository.findAll();
    }

    public Optional<Localisation> getLocalisationById(String id) {
        return localisationRepository.findById(id);
    }

    public void deleteLocalisation(String id) {
        localisationRepository.deleteById(id);
    }
}
