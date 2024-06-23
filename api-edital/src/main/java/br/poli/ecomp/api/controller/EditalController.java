package com.example.edital.controller;

import com.example.edital.model.Edital;
import com.example.edital.service.EditalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/editais")
public class EditalController {

    @Autowired
    private EditalService editalService;

    @GetMapping
    public List<Edital> getAllEditais() {
        return editalService.getAllEditais();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Edital> getEditalById(@PathVariable Long id) {
        return editalService.getEditalById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Edital createEdital(@RequestBody Edital edital) {
        return editalService.saveEdital(edital);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Edital> updateEdital(@PathVariable Long id, @RequestBody Edital editalDetails) {
        return editalService.getEditalById(id)
                .map(edital -> {
                    edital.setTitulo(editalDetails.getTitulo());
                    edital.setDescricao(editalDetails.getDescricao());
                    edital.setDataPublicacao(editalDetails.getDataPublicacao());
                    edital.setDataEncerramento(editalDetails.getDataEncerramento());
                    Edital updatedEdital = editalService.saveEdital(edital);
                    return ResponseEntity.ok(updatedEdital);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEdital(@PathVariable Long id) {
        if (editalService.getEditalById(id).isPresent()) {
            editalService.deleteEdital(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}
