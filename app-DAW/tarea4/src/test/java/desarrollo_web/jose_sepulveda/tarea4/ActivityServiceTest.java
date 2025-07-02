package desarrollo_web.jose_sepulveda.tarea4;

import desarrollo_web.jose_sepulveda.tarea4.services.ActivityService;
import desarrollo_web.jose_sepulveda.tarea4.services.ActivityDto;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class ActivityServiceTest {

    @Autowired
    private ActivityService activityService;

    @Test
    void testFinishedActivities() {
        List<ActivityDto> finished = activityService.finished();
        // No se espera una cantidad exacta, pero sí que no sea nulo
        assertThat(finished).isNotNull();
        // Si tienes datos de prueba puedes hacer más validaciones
        finished.forEach(dto ->
            assertThat(dto.fechaInicio()).isBeforeOrEqualTo(dto.fechaInicio()));
    }
}
