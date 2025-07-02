package desarrollo_web.jose_sepulveda.tarea4.controllers;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import desarrollo_web.jose_sepulveda.tarea4.services.ActivityDto;
import desarrollo_web.jose_sepulveda.tarea4.services.ActivityService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

@RestController @RequestMapping("/api/activities")
public class ActivityController {
    private final ActivityService service;
    public ActivityController(ActivityService service) {
        this.service = service;
    }

    @GetMapping("/finished")
    public List<ActivityDto> finished() { return service.finished(); }

    public record NotePayload(
        @Min(1) @Max(7) Integer valor) { }

    @PostMapping("/{id}/notes")
    public ResponseEntity<ActivityDto> agregarNota(
            @PathVariable long id,
            @RequestBody @Valid NotePayload body) {

        ActivityDto dto = service.addNote(id, body.valor());
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(dto);
    }
}